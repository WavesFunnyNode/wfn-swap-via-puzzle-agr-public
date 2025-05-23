import requests
import pywaves as pw
import time

# connects to a local or public mainnet node
NodeAPI = 'https://nodes.wavesnodes.com'

pw.setNode(node=f'{NodeAPI}', chain='mainnet')

# Wallet
myAddress = pw.Address(privateKey='####')  # private key from the wallet

# get address from private key above 
AddressFromPywaves = myAddress.address

# Replace these values with your actual tokens and amount
TOKEN1ID = 'Atqv59EYzjFGuitKVnMRk6H8FukjoV3ktPorbEys25on'
TOKEN2ID = 'WAVES'
MaxSlippage = 0.95 # How much will be received after the swap, e.g., 5% less? If it exceeds the desired amount, the swap will be canceled
divider = 1  # Set the desired divisor, e.g., 5, to swap 1/5 of the amount.
AmountOfSomeFee = 0.10 # how much % to be deducted from the total amount
PuzzleAgrFee = 0.9974 # 0.26% fee for puzzle aggregator

#! If wanna remove fixed amount everytime don't forget to uncomment "somefee" and put a amount of "AmountOfSomeFee"

# Fetch balance based on TOKEN1ID
if TOKEN1ID == "WAVES":
    # Fetch available balance from the Waves Node API
    waves_balance_response = requests.get(f'{NodeAPI}/addresses/balance/details/{AddressFromPywaves}')
    
    # Check if the request was successful (status code 200)
    if waves_balance_response.status_code == 200:
        # Parse the response JSON
        waves_balance_result = waves_balance_response.json()
        # Extract the available balance
        waves_balance = waves_balance_result.get('available', 0)
        
        # Set amount of available balance following divider, somefee rules
        preAmount = waves_balance // divider
        somefee = int(preAmount * AmountOfSomeFee)
        # If you want to remove a fixed amount every time, comment above and uncomment 'somefee' below.
        # somefee = PreAmount - AmountOfSomeFee
        amount = preAmount - somefee
    else:
        print(f"Error fetching Waves balance: {waves_balance_response.status_code} - {waves_balance_response.text}")
        # Set a default amount if the request fails
        preAmount = myAddress.balance() // divider
        somefee = int(preAmount * AmountOfSomeFee)
        # If you want to remove a fixed amount every time, comment above and uncomment 'somefee' below.
        # somefee = PreAmount - AmountOfSomeFee
        amount = preAmount - somefee
else:
    # Set amount of token balance following divider, somefee rules
    preAmount = myAddress.balance(TOKEN1ID) // divider
    somefee = int(preAmount * AmountOfSomeFee)
    # If you want to remove a fixed amount every time, comment above and uncomment 'somefee' below.
    # somefee = PreAmount - AmountOfSomeFee
    amount = preAmount - somefee

print(f"Amount after divider & somefee:", amount)
print(" ")

# API URL of Puzzle ARG
api_url = f"https://swapapi.puzzleswap.org/aggregator/calc?token0={TOKEN1ID}&token1={TOKEN2ID}&amountIn={amount}"

# Add headers directly to the API URL
# headers = {'Authorization': 'Bearer IIqbbwzJLdDKiOWvVTwaBEVSXzAjtd'}

try:
    # Make the API request
    response = requests.get(api_url)  #, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        result = response.json()

        # Check if "parameters" key is present in the response
        if "parameters" in result:
            parameters = result["parameters"]
            print("Parameters:", parameters)
            print(" ")
            
        # Check if "estimatedOut:" key is present in the response
        if "estimatedOut" in result:
            estimatedOut = result["estimatedOut"]
            print("estimatedOut:", estimatedOut)
            print(" ")
            
            # Ensure that parameters is a string
            parameters_str = str(parameters)

            # Introduce a 1-second delay
            time.sleep(1)

            # Proceed with the swap
            PuzzleSwapaddress = '3PGFHzVGT4NTigwCKP1NcwoXkodVZwvBuuU'  
            fee = 500000  # DEFAULT_INVOKE_SCRIPT_FEE - Waves
            MinToReceive = int((estimatedOut * MaxSlippage) * PuzzleAgrFee)

            # Determine assetId based on TOKEN1ID
            assetId = TOKEN1ID if TOKEN1ID != "WAVES" else None

            tx = myAddress.invokeScript(PuzzleSwapaddress, 'swapWithReferral',
                                        params=[{"type": "string", "value": parameters_str},
                                                {"type": "integer", "value": MinToReceive},
                                                {"type": "string", "value": 'wfn'}],
                                        payments=[{"assetId": assetId, "amount": amount}],  # ! if is not waves - assetId: TokenID1
                                        feeAsset=None, txFee=fee)
            
            print(" ")
            print("Swap invoked. Transaction ID:", tx)
            print(" ")

        else:
            print("Error: 'parameters' key not found in the response")

    else:
        print(f"Error: {response.status_code} - {response.text}")

except Exception as e:
    print(f"An error occurred: {e}")
    print(response)
    print(result)