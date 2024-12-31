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
import ipaddress

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
        replacement = hash10(email.split('@')[0], size=6) + '@' + email.split('@')[-1]
        text = re.compile(email).sub(replacement, text)
    return text

def replace_ipv4_addresses(text):
    ''' Replace non-private IPv4 addresses '''
    ipv4_pattern = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}')
    for match in re.finditer(ipv4_pattern, text):
        ip = match.group()
        try:
            ip_obj = ipaddress.ip_address(ip)
            if not ip_obj.is_private:  # Only replace non-private IPs
                replacement = hash10(ip, size=8)
                text = re.compile(ip).sub(replacement, text)
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
        ip = match.group()
        if len(ip) < 10:
            continue
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.version == 6 and not ip_obj.is_private:  # Only replace non-private IPv6
                replacement = hash10(ip, size=12)  # Generate a replacement hash
                text = re.compile(re.escape(ip)).sub(replacement, text)
        except ValueError:
            continue  # Skip invalid IPv6 addresses
    return text

def replace_payment_card_numbers(text):
    ''' Replace valid payment card numbers (with Luhn checksum validation) '''
    card_pattern = re.compile(r'\b(?:\d[ -]*?){13,19}\b')  # Match potential card numbers

    def luhn_checksum(card_number):
        ''' Validate the Luhn checksum of a card number '''
        digits = [int(d) for d in card_number if d.isdigit()]
        checksum = 0
        reverse_digits = digits[::-1]
        for i, d in enumerate(reverse_digits):
            if i % 2 == 1:  # Double every second digit
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        return checksum % 10 == 0

    for match in re.finditer(card_pattern, text):
        card_number = match.group().replace(' ', '').replace('-', '')  # Normalize card number
        if luhn_checksum(card_number):  # Validate with Luhn
            replacement = hash10(card_number, size=12)  # Replace with hashed value
            text = re.compile(re.escape(match.group())).sub(replacement, text)
    return text

def protect_privacy(filepath):
    ''' Replace private information '''
    text = read_file(filepath)  # Read the file
    text = replace_email_addresses(text)
    text = replace_ipv4_addresses(text)
    text = replace_payment_card_numbers(text)
    text = replace_ipv6_addresses(text)
    write_file(filepath + '.protected', text)  # Write the modified content back to the file

def main():
    ''' Call privacy protection over the text files passed as command-line arguments '''
    parser = argparse.ArgumentParser(description='Apply privacy protection to text files.')
    parser.add_argument(
        'files',
        nargs='+',
        help="List of file paths or patterns to process (e.g., 'English/textpages/*.txt').",
    )
    args = parser.parse_args()

    for path in args.files:
        # Use glob to expand patterns like '*.txt'
        for filepath in glob.glob(path):
            protect_privacy(filepath)

if __name__ == '__main__':
    main()
