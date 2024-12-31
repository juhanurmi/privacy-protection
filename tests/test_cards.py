import pytest
from unittest.mock import patch
from privacy_protection import protect_privacy

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_credit_card(mock_write, mock_read):
    """Test the replace_payment_card_numbers function."""
    mock_read.return_value = "My card numbers are 4111 1111 1111 1111 and 5500-0000-0000-0004. Invalid: 4111 1111 1111 1112."
    protect_privacy("dummy.txt")
    expected_output = (
        "My card numbers are card-3aeedea8fef2 and card-3b49ffea0e53. Invalid: 4111 1111 1111 1112."
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)
