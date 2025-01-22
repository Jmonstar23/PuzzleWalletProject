import itertools
import bip39
import blockcypher
import logging

# Updated to validate permutations by checking BIP39 checksum instead of the generate and check blockchain method originally used

# Configure logging
logging.basicConfig(filename='bruteForceBTC.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# List of words (replace with your actual words)
prefix_words = ["head", "honey", "bitter", "find", "sock", "dash"]
restricted_words = {"bridge": 7, "current": 8}  # Words with restricted positions
main_words = ["tail", "bottom", "culture", "arrive", "addict", "fish", "inch", "like", "pass", "coin", "matter", "bridge", "current"]
valid_3letter = ["web", "all", "cry", "car", "way", "act", "arm", "rib", "one", "sea"]  # 5 of these 10 words should be used for each 24 word combo per key phrase attempt

# Function to generate Bitcoin address from a key phrase
def generate_address(key_phrase):
    seed = bip32utils.BIP32Key.fromEntropy(key_phrase.encode())
    address = seed.Address()
    return address

# Function to check the balance of a Bitcoin address
def check_balance(address):
    balance = blockcypher.get_address_overview(address, coin_symbol='btc')
    return balance['final_balance']

# Function to check if a key phrase has a valid BIP39 checksum
def is_valid_bip39(key_phrase):
    return bip39.validate_mnemonic(key_phrase)

# Generate all possible combinations of the main words and valid 3-letter words
all_words = main_words + valid_3letter
combinations = list(itertools.permutations(all_words, 18))

# Filter combinations to ensure restricted words are present and not in their restricted positions
filtered_combinations = []
for combo in combinations:
    valid = True
    for word, pos in restricted_words.items():
        if word not in combo or combo[pos - 7] == word:  # Adjust position for 0-based index and prefix offset
            valid = False
            break
    if valid:
        filtered_combinations.append(combo)

# Check each combination
for combo in filtered_combinations:
    key_phrase = prefix_words + list(combo)
    key_phrase_str = " ".join(key_phrase)
    
    if is_valid_bip39(key_phrase_str):
        address = generate_address(key_phrase_str)
        balance = check_balance(address)
        
        # Log the key phrase, address, and balance
        logging.info(f"Key Phrase: {key_phrase_str}")
        logging.info(f"Bitcoin Address: {address}")
        logging.info(f"Balance: {balance}")
        
        if balance > 0:
            print("Found balance!")
            print("Key Phrase:", key_phrase_str)
            print("Bitcoin Address:", address)
            print("Balance:", balance)
            break
