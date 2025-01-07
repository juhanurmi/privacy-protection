# -*- coding: utf-8 -*-
'''
Privacy protection:
Replace fields with random IDs; keep the same ID for the same address through the dataset.
'''
import os
import re
import random
import argparse
import hashlib
import glob
import json
import ipaddress
import spacy # pylint: disable=import-error

field_list = ['ipv4', 'ipv6', 'card', 'iban', 'email', 'name', 'location']

nlp = spacy.load('en_core_web_sm') # Load English NLP model

def random_string(size=700):
    ''' Return a random string, default size is 700 '''
    # Total of 64 options: Letters (upper and lower cases) + digits + -_
    # Strength: 64^size = (2^6)^size = 2^(6*size)
    # Short salt size 2: 2^12 = 4096 different salts.
    # Medium salt size 6: 2^36 = 68 719 476 736 different salts.
    # Strong sufficient salt size is 42 or larger:  2^252 different salts.
    # Very strong salt size 700: 2^4200 different salts.
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    return ''.join(random.choice(chars) for index in range(size))

RANDOM_SALT = random_string() # One salt for the dataset

def hash10(text, size=8):
    ''' Hash the text with salt. Return a sub string of the hash. '''
    text_salt = text.encode('utf-8') + RANDOM_SALT.encode('utf-8')
    hashed_string = hashlib.sha512(text_salt).hexdigest()
    return hashed_string[0:size] # Only 8 first letters

def read_file(filename):
    ''' Read a file and return the text '''
    content = ''
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as myfile:
            content = myfile.read()
    return content

def write_file(filename, content):
    ''' Write the text to a file '''
    with open(filename, 'w', encoding='utf-8') as myfile:
        myfile.write(content)

def replace_email_addresses(text):
    ''' Replace email addresses '''
    email_pattern = re.compile(r'[a-zA-Z0-9._-]{2,25}@[a-zA-Z0-9.-]{2,25}\.[a-zA-Z]{2,10}')
    for match in re.finditer(email_pattern, text):
        email = match.group()
        if any(True for field in field_list if f'{field}-' in email):
            continue
        replacement = 'email-' + hash10(email.split('@')[0], size=6) + '@' + email.split('@')[-1]
        print(f'Replace: {email} --> {replacement}')
        text = re.compile(email).sub(replacement, text)
    return text

def replace_ipv4_addresses(text):
    ''' Replace non-private IPv4 addresses '''
    ipv4_pattern = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}')
    for match in re.finditer(ipv4_pattern, text):
        ip_addr = match.group()
        try:
            ip_obj = ipaddress.ip_address(ip_addr)
            if not ip_obj.is_private:  # Only replace non-private IPs
                replacement = 'ipv4-' + hash10(ip_addr, size=8)
                print(f'Replace: {ip_addr} --> {replacement}')
                text = re.compile(ip_addr).sub(replacement, text)
        except ValueError:
            continue  # Skip invalid IPs
    return text

def replace_ipv6_addresses(text):
    ''' Replace valid, non-private IPv6 addresses '''
    ipv6_pattern = re.compile(
        r'(?<![:\w])('
        r'(?:[a-fA-F0-9]{1,4}:){1,7}[a-fA-F0-9]{1,4}|'  # Standard format
        r'(?:[a-fA-F0-9]{1,4}:){1,7}:|'                # Trailing double colon
        r':[a-fA-F0-9]{1,4}|'                          # Leading double colon
        r'(?:[a-fA-F0-9]{1,4}:){1,6}::[a-fA-F0-9]{1,4}|'  # Embedded double colon
        r'::(?:[a-fA-F0-9]{1,4}:){1,6}[a-fA-F0-9]{1,4}|' # Double colon with trailing
        r'::'                                           # Only double colon
        r')(?![:\w])'
    )
    for match in re.finditer(ipv6_pattern, text):
        ip_addr = match.group()
        if len(ip_addr) < 10:
            continue
        try:
            ip_obj = ipaddress.ip_address(ip_addr)
            if ip_obj.version == 6 and not ip_obj.is_private:  # Only replace non-private IPv6
                replacement = 'ipv6-' + hash10(ip_addr, size=12)  # Generate a replacement hash
                print(f'Replace: {ip_addr} --> {replacement}')
                text = re.compile(re.escape(ip_addr)).sub(replacement, text)
        except ValueError:
            continue  # Skip invalid IPv6 addresses
    return text

def replace_payment_card_numbers(text):
    ''' Replace valid payment card numbers (with Luhn checksum validation) '''
    card_pattern = re.compile(r'\b(?:\d[ -]*?){13,19}\b')  # Match potential card numbers

    def luhn_checksum(card_number):
        ''' Validate the Luhn checksum of a card number '''
        digits = [int(digit) for digit in card_number if digit.isdigit()]
        checksum = 0
        reverse_digits = digits[::-1]
        for index, digit in enumerate(reverse_digits):
            if index % 2 == 1:  # Double every second digit
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        return checksum % 10 == 0

    for match in re.finditer(card_pattern, text):
        card_match = match.group()
        card_number = card_match.replace(' ', '').replace('-', '')  # Normalize card number
        if luhn_checksum(card_number):  # Validate with Luhn
            replacement = 'card-' + hash10(card_number, size=12)  # Replace with hashed value
            print(f'Replace: {card_match} --> {replacement}')
            text = re.compile(re.escape(match.group())).sub(replacement, text)
    return text

def replace_iban_with_ids(text):
    ''' Replace IBANs (based on ISO 13616 standard) in text with unique IDs '''
    iban_pattern = re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}\b')
    for match in re.finditer(iban_pattern, text):
        iban = match.group()
        replacement = f'iban-{hash10(iban, size=12)}'
        print(f'Replace: {iban} --> {replacement}')
        text = text.replace(iban, replacement)
    return text

def replace_names_with_ids_ner(text, doc):
    ''' Find and replace human names with unique IDs using NER '''
    for ent in doc.ents:
        if any(True for field in field_list if f'{field}-' in ent.text):
            continue
        if any(True for field in ['=', '<', '>', '"', "'"] if field in ent.text):
            continue
        if ent.label_ == "PERSON":  # Only replace names tagged as PERSON
            replacement = f'name-{hash10(ent.text, size=12)}'
            print(f'Replace: {ent.text} --> {replacement}')
            text = text.replace(ent.text, replacement)
    return text

def replace_locations_with_ids(text, doc):
    ''' Find and replace locations (GPE and LOC) with unique IDs '''
    for ent in doc.ents:
        if any(True for field in field_list if f'{field}-' in ent.text):
            continue
        if any(True for field in ['=', '<', '>', '"', "'"] if field in ent.text):
            continue
        if ent.label_ in ["GPE", "LOC"]:  # Replace geographical locations
            replacement = f'location-{hash10(ent.text, size=12)}'
            print(f'Replace: {ent.text} --> {replacement}')
            text = text.replace(ent.text, replacement)
    return text

def replacements(text, protect):
    ''' Call replacements selectively based on protect argument '''
    if 'email' in protect:
        text = replace_email_addresses(text)
    if 'ipv4' in protect:
        text = replace_ipv4_addresses(text)
    if 'ipv6' in protect:
        text = replace_ipv6_addresses(text)
    if 'card' in protect:
        text = replace_payment_card_numbers(text)
    if 'iban' in protect:
        text = replace_iban_with_ids(text)
    if 'name' in protect or 'location' in protect:
        doc = nlp(text)  # Create a spaCy document
        if 'name' in protect:
            text = replace_names_with_ids_ner(text, doc)
        if 'location' in protect:
            text = replace_locations_with_ids(text, doc)
    return text


def process_json(data, protect):
    ''' Recursively process JSON fields to replace PII '''
    if isinstance(data, dict):  # If the data is a dictionary, process its keys and values
        for key, value in data.items():
            data[key] = process_json(value, protect)
    elif isinstance(data, list):  # If the data is a list, process each element
        data = [process_json(item, protect) for item in data]
    elif isinstance(data, str):  # If the data is a string, process it for PII
        data = replacements(data, protect)
    return data


def protect_privacy(filepath, protect=None):
    ''' Replace private information selectively '''
    if protect is None:  # Initialize protect with the default field list
        protect = field_list
    if filepath.endswith('.json'):
        # Handle JSON files
        with open(filepath, 'r', encoding='utf-8') as myfile:
            data = json.load(myfile)  # Load JSON data
        processed_data = process_json(data, protect)  # Process JSON recursively
        with open(filepath + '.protected', 'w', encoding='utf-8') as myfile:
            json.dump(processed_data, myfile, ensure_ascii=False, indent=4)  # Write modified JSON
    else:
        # Handle plain text files
        text = read_file(filepath)
        text = replacements(text, protect)
        write_file(filepath + '.protected', text)  # Write the modified content back to the file


def main():
    ''' Call privacy protection over the text files passed as command-line arguments '''
    parser = argparse.ArgumentParser(
        description='Apply privacy protection to text files. Specify what PII to protect.'
    )
    parser.add_argument(
        '-p', '--protect',
        type=str,
        default='all',
        help="Comma-separated list of PII types to protect (e.g., 'email,ipv4,name'). "
             "Options: email, ipv4, ipv6, card, iban, name, location. Default: 'all'."
    )
    parser.add_argument(
        'files',
        nargs='+',
        help="List of file paths or patterns to process (e.g., 'examples/*.txt')."
    )
    args = parser.parse_args()

    # Parse the protect argument
    ops = field_list
    if args.protect == 'all':
        protect = ops
    else:
        protect = [item.lower().strip() for item in args.protect.split(',')]
        invalid_options = [item for item in protect if item not in ops]
        if invalid_options:
            parser.error(f"Invalid protect option(s): {', '.join(invalid_options)}. "
                         f"Valid options are: {', '.join(ops)}.")

    # Process the files
    for path in args.files:
        for filepath in glob.glob(path):  # Use glob to expand patterns
            protect_privacy(filepath, protect)


if __name__ == '__main__':
    main()
