import pytest
from unittest.mock import patch
from privacy_protection import protect_privacy

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_names(mock_write, mock_read):
    """Test the protect_privacy function."""
    mock_read.return_value = "My IBAN is DE89370400440532013000."
    protect_privacy("dummy.txt")
    expected_output = (
        "My IBAN is iban-2aa25e938c90."
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)
