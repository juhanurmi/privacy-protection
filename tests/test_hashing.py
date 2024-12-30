import pytest
from unittest.mock import patch
from privacy_protection import hash10

@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_hash10():
    """Test the hash10 function."""
    input_text = "test_email"
    result = hash10(input_text, size=8)
    assert len(result) == 8
    assert result == "cf3df552"
