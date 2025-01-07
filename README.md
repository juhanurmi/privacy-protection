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
Names: Juha Nurmi, David Arroyo, ...
My IBAN is DE89370400440532013000.

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

Emails: email-06ba83@example.com or name-91a27ebb34ee or email-12f502@gmail.com
IPv4: ipv4-2f02983c and ipv4-4ab823ca. Private 10.0.0.0/8 and 127.0.0.1.
IPv6: ipv6-a61ed9b1ac7f ==> ipv6-17c6166ae885
My card numbers are card-3d99e050f21e and card-76ae34ad641e.
Names: name-04f9cd316951, name-9a16734c3b67, ...
My IBAN is iban-b5478106641f.

Copyright (c) 2024 name-04f9cd316951
location-22b3bcd54ec5
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

The privacy protection software creates new files and replaces all PII by default (`python privacy_protection.py examples/*.json examples/example.txt`).

Also, it is possible to select which PII information to replace.

```
python privacy_protection.py --protect email,ipv4,ipv6,card,iban,name,location examples/example.txt

Replace: user@example.com --> email-739ab3@example.com
Replace: admin@uk.eu --> email-ce1216@uk.eu
Replace: 21789@gmail.com --> email-dc01cc@gmail.com
Replace: 216.58.211.238 --> ipv4-51451b13
Replace: 74.6.231.20 --> ipv4-a3fad872
Replace: 2345:0425:2CA1:0000:0000:0567:5673:23b5 --> ipv6-cc5ebd88497e
Replace: 2345:0425:2CA1:0:0:0567:5673:23b5 --> ipv6-88f8da9b4eee
Replace: 4111 1111 1111 1111 --> card-e8d2c857fa61
Replace: 5500-0000-0000-0004 --> card-0ae0d4fff6a5
Replace: DE89370400440532013000 --> iban-90eb12ae7269
Replace: Juha Nurmi --> name-d4da01292708
Replace: David Arroyo --> name-1d9107438fbe
Replace: Juha Nurmi --> name-d4da01292708
Replace: Finland --> location-aa6977909879
```
