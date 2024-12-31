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
Full name
Passport information
Social Security number (SSN)

Emails: user@example.com or admin@uk.eu or 21789@gmail.com
IPv4: 216.58.211.238 and 74.6.231.20. Private 10.0.0.0/8 and 127.0.0.1.
IPv6: 2345:0425:2CA1:0000:0000:0567:5673:23b5 ==> 2345:0425:2CA1:0:0:0567:5673:23b5
My card numbers are 4111 1111 1111 1111 and 5500-0000-0000-0004.
Names: Juha Nurmi, Constantinos Patsakis, David Arroyo, ...

Copyright (c) 2024 Juha Nurmi
Finland
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

Emails: email-89cbec@example.com or email-e31dec@uk.eu or email-a535f5@gmail.com
IPv4: IPv4-deed46b2 and IPv4-99a61afd. Private 10.0.0.0/8 and 127.0.0.1.
IPv6: IPv6-37ad83cb6438 ==> IPv6-7ca162e4ca59
My card numbers are card-c59007e80cc9 and card-5a9de5f7fb51.
Names: name-275b08d538e2, name-2fe5cd841519, name-3f56e67eb0cc, ...

Copyright (c) 2024 name-275b08d538e2
location-cd9fa5a19c93
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
