#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 00:16:41 2025

@author: Jmon (Guided by Bing's Ai ChatGPT4 Model')
"""
# Import necessary modules

import itertools
import bip39
import bip32utils
import blockcypher
import logging

#   Latest version of 24word key-phrase brute forcer for cracking the puzzle wallet
# from [https://allcoins.pw] This latest version has been optimized by dropping the
# full process for every combo, no longer generating wallet and requesting blockchain 
# data and instead using the BIP39 checksum feature to quickly determine if the 
# permutation is a valid key-phrase. One a valid phrase is permutated, then the keys 
# will be generated, then its data will be requested from the blockchain.

jmonBanner = print("""
        
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░^░░░░░░░
        ░░░╔════════════╗╔══════╗░░░╔══════╗░░░░╔═════╗░░░░╔═════╗░░░╔═════╗░░░░░░░░░//\░░░░░
        ░░░║████████████║║██████╚╗░╔╝██████║░╔══╝█████╚══╗░║█████╚╗░░║█████║░░░░░░░░///\\░░░
        ░░░╚═╝░░║███║░╚═╝░║███╠╗██╬██╔╣███║╔╝███╔╝░░░╚╗███╚╗║███╔╗██╚╗║███║░░░░\\\\██████░░░░
        ░╔═══╗░░║███║░░░░░║███║╚╗███╔╝║███║║███╬╣░░░░░╠╬███║║███║╚╗██╚╣███║░░░░░\\\\████/░░░░░
        ░║███╚╗╔╝███║░░░░░║███║░╚╗█╔╝░║███║╚╗███╚╗░░░╔╝███╔╝║███║░╚╗██╬███║░░░░░░\\\\██//░░░░░
        ░╚╗███╚╝███╔╝░░░░╔╝███╚╗░╚═╝░╔╝███╚╗╚╗███╚═══╝███╔╝╔╝███╚╗░╚╗█████╚╗░░░░░////////░░░░
        ░░╚═╗████╔═╝░░░░░║█████║░░░░░║█████║░╚══╗█████╔══╝░║█████║░░╚╗█████║░░░░/////////░░░
        ░░░░╚════╝░░░░░░░╚═════╝░░░░░╚═════╝░░░░╚═════╝░░░░╚═════╝░░░╚═════╝░░░//////////░░░░
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        Made by Jmon & ChatGPT
        """)

# Configure Logging

logging.basicConfig(filename='bruteForceBTCpuzzle.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# List of words to use

prefix = ["head", "honey", "bitter", "find", "sock", "dash"]
knownAntiPos = {"bridge": 7, "current": 8} ## ^^ Words we KNOW where they do NOT go ^^ ##
segment_words = ["tail", "bottom", "matter", "like", "arrive", "addict", "fish", "inch", "bridge", "current"]
suffix_words = ["breath", "fight", "passenger", "segway", "gimmick", "allcoins", "crypto", "website"] # 5 of these 10 should be used per 24word phrase

## Upon reading the challenge info again, focusing on literal word choices in desc. it may be necessary 
## to bring back the non-BIP39 extra-security words found in the puzzle. Prev removed non-BIP words due 
## to misremembering exact words on whether or not only BPI39 words were used or not. Some words were 
## removed, some had valid sub-words that were extracted and are in use. The removed words/parts on next lines:
#  | all>=>allcoins | web>=>website | way>=>segway | pass>=>passenger | 
#  Fully Redacted: gimmick | breath | 
# STANDBY: More words found... will revamp word lists soon!


# Function to generate Bitcoin addresses from a key phrase
def gen_address(key_phrase):
    seed = bip32utils.BIP32Key.fromEntropy(key_phrase.encode())
    address = seed.Address()
    return address

# Function to check the balance of a Bitcoin address
def check_balance(address):
    balance = blockcypher.get_address_overview(address, coin_symbol='btc')
    return balance['final_balance']
    
# Function to check if a key-phrase has a valid BIP39 checksum
def is_valid_bip39(key_phrase):
    return bip39.validate_mnemonic(key_phrase)

##       Old Code, comment and code commented out and replaced
## Generate all possible combinations of the main words and the 3letter words    
##all_words = mainWords + triLetter
##combinations = list(itertools.permutations(all_words, 18))

##      New Code as follows:


# Generate all possible combinations of the segment words for indexes 7-12
segment_combos = list(itertools.permutations(segment_words, 6))





# Filter segment Combinations to ensure restricted words are present and not in their restricted postitions
filtered_segment_combos = []
for combo in segment_combos:
    valid = True
    for word, pos in knownAntiPos.items():
        if word not in combo or combo[pos - 7] == word:  # neg -7 for # (6) of prefixed words plus -1 for zero-based indexing (0,1,2,3,etc) 
            valid = False
            break
        if valid:
            filtered_segment_combos.append(combo)

## Check each combination
##for combo in filtered_combinations:
##    key_phrase = prefix + list(combo)
##    key_phrase_str = " ".join(key_phrase)

# Check each combo
for segment_combo in filtered_segment_combos:
    remaining_words = set(segment_words) - set(segment_combo)
    remaining_words.update(suffix_words)

    # Generate all possible combos of the remaining words for indexes 13-24
    suffix_combos = list(itertools.permutations(remaining_words, 12))
    
    for suffix_combo in suffix_combos:
        key_phrase = prefix + list(segment_combo) + list(suffix_combo)
        key_phrase_str = " ".join(key_phrase)


    
        if is_valid_bip39(key_phrase_str):
            address = gen_address(key_phrase_str)
            balance = check_balance(address)
        
            # Log the key phrase, address, and balance
            logging.info(f"Key Phrase: {key_phrase_str}")
            logging.info(f"Bitcoin Address: {address}")
            logging.info(f"Balance: {balance}")

            if balance > 0:
                print("Found Balance!!!!!")
                print("Key Phrase:", key_phrase_str)
                print("Bitcoin Address:", address)
                print("Balance:", balance, "!!!!!")
                print(jmonBanner)
                break
            
    
    
    