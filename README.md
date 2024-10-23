# WFN Swaps via Puzzle AGR

System preparation:
```
sudo apt install build-essential
sudo apt install python3-dev
sudo apt install python3-pip
sudo apt install python3-testresources
pip3 install pywaves
```

## Introduction
This Python script provides a simple and intuitive interface for interacting with the Waves blockchain, facilitating token swaps with customizable parameters.

The tool facilitates swaps through Puzzle ARG. By leveraging the open API of the puzzle-backed tool, seize the opportunity to fetch the optimal route for TokenID1 and TokenID2. Subsequently, employ these parameters in the invoke-command using PyWaves to execute the swap through the Puzzle dApp.


## About tool features:
- Max Slippage (default is -5% of the amount of TokenID2).
- Divide the amount to be swapped (TokenID1).
- You can choose the percentage (or the fixed amount) from the TokenID1 amount to be deducted
- All calculations are based on TokenID1. For example, if it is "WAVES," it will fetch the effective balance of the wallet. If it is some token ID, it will fetch the amount of this token ID using PyWaves.

## 1. Configure your settings:
```python

# Set Node API
pw.setNode(node='http://##.##.##.##:##', chain='mainnet')

# Initialize wallet with private key
myAddress = pw.Address(privateKey='####')

# Define tokens for swapping
TOKEN1ID = 'WAVES'  # Token used for swapping with another token
TOKEN2ID = 'Atqv59EYzjFGuitKVnMRk6H8FukjoV3ktPorbEys25on'  # Token intended to be received after the swap

# Set swap parameters
MaxSlippage = 0.95  # Maximum acceptable slippage for the swap
divider = 1  # Set the desired divisor, e.g., 5, to swap 1/5 of the amount
AmountOfSomeFee = 0.10  # Percentage of total amount to be deducted as a fee, e.g., 10%
PuzzleAgrFee = 0.9974 # (fixed fee) 0.26% for puzzle aggregator
```

#### Using the tool

```
python3 puzzle-arg-cacl-and-swap.py
```

#### Have questions, or need help?
Welcome to ask anytime!:
- Puzzle: https://t.me/puzzle_network
- WavesFunnyNode: https://t.me/wavesfunnynode

#### No secrets 
_The incorporation of a referral code within the tool not only enhances the current functionality but also serves as a valuable contribution towards the ongoing development and maintenance of similar tools in the future. Your support through the referral code is instrumental in fueling our commitment to expanding and refining our toolset for continued utility and innovation_
