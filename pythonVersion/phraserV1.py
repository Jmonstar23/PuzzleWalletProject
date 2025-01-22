import itertools
import bip32utils
import blockcypher
import logging

# Configure logging
logging.basicConfig(filename='bruteForceBTC.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# List of words (replace with your actual words)
prefix_words = ["head", "honey", "bitter", "find", "sock", "dash"]
restricted_words = {"bridge": 7, "current": 8}  # Words with restricted positions(must be added to main_words)
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

# Generate all possible combinations of the main words

placeholders = ["v1", "v2", "v3", "v4", "v5"]
all_words = main_words + placeholders
combinations = list(itertools.permutations(all_words, len(all_words)))

# Filter combinations to ensure restricted words are not in their restricted positions
filtered_combinations = []
for combo in combinations:
    valid = True
    for word, pos in restricted_words.items():
        if combo[pos - 7] == word:  # Adjust position for 0-based index and prefix offset
            valid = False
            break
    if valid:
        filtered_combinations.append(combo)

# Function to generate all possible key phrases with valid 3-letter words
def generate_key_phrases(template, extra_words):
    from itertools import combinations
    key_phrases = []
    for combo in combinations(extra_words, 5):
        key_phrase = template.copy()
        for i, word in enumerate(combo):
            key_phrase[i] = word
        key_phrases.append(" ".join(key_phrase))
    return key_phrases

# Check each combination
for combo in filtered_combinations:
    key_phrase = prefix_words + list(combo)
    key_phrase_str = " ".join(key_phrase)
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
