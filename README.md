# privacy-protection

Replace fields with random IDs; keep the same ID for the same address through the datasets.
Protect technical personal identifiable information, including
IPv4 addresses, payment card numbers, email addresses, etc.

## Example

Input:

```
This is an example text file with Personally Identifiable Information (PII), such as:

Email address
IP address
Credit card information
Date of birth
Financial information
Full name
Passport information
Social Security number (SSN)

Emails: user@example.com or admin@uk.eu or 21789@gmail.com
IPv4: 216.58.211.238 and 74.6.231.20. Private 10.0.0.0/8 and 127.0.0.1.
IPv6: 2345:0425:2CA1:0000:0000:0567:5673:23b5 ==> 2345:0425:2CA1:0:0:0567:5673:23b5
My card numbers are 4111 1111 1111 1111 and 5500-0000-0000-0004.
Names: Juha Nurmi, David, and Constantinos.

Copyright (c) 2024 Juha Nurmi
```

Output:

```
This is an example text file with Personally Identifiable Information (PII), such as:

Email address
IP address
Credit card information
Date of birth
Financial information
Full name
Passport information
Social Security number (SSN)

Emails: email-0a4505@example.com or email-5cbd64@uk.eu or email-f31ccf@gmail.com
IPv4: IPv4-9e4b30f3 and IPv4-8657c497. Private 10.0.0.0/8 and 127.0.0.1.
IPv6: IPv6-b17d0a3ba114 ==> IPv6-cba19534cad4
My card numbers are card-09f3aad1fd66 and card-88b823ab71f9.
Names: name-163b4411e57e, name-c349d640d510, and name-29f5d0b936c3.

Copyright (c) 2024 name-163b4411e57e
```

## Install

```
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Tests

```
export PYTHONPATH=$(pwd)
pytest tests/
```

## Usage

```
python privacy_protection.py examples/*.json examples/example.txt
```
