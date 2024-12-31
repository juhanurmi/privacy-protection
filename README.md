# privacy-protection

Replace fields with random IDs; keep the same ID for the same address through the datasets.

Protect technical personal identifiable information, including
IPv4 addresses, payment card numbers, email addresses, etc.

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
