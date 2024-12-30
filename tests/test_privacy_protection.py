import pytest
from unittest.mock import patch
from privacy_protection import protect_privacy

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_email_addresses(mock_write, mock_read):
    """Test the protect_privacy function."""
    mock_read.return_value = "user@example.com or admin@uk.eu or 21789@gmail.com"
    protect_privacy("dummy.txt")
    expected_output = (
        "6a9841@example.com or 67d73c@uk.eu or dd0169@gmail.com"
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_ipv4(mock_write, mock_read):
    """Test the protect_privacy function."""
    mock_read.return_value = "Private 10.0.0.0/8 and 172.16.0.0/12 and 192.168.0.0/16."
    protect_privacy("dummy.txt")
    expected_output = (
        "Private 10.0.0.0/8 and 172.16.0.0/12 and 192.168.0.0/16."
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_credit_card(mock_write, mock_read):
    """Test the replace_payment_card_numbers function."""
    mock_read.return_value = "My card numbers are 4111 1111 1111 1111 and 5500-0000-0000-0004. Invalid: 4111 1111 1111 1112."
    protect_privacy("dummy.txt")
    expected_output = (
        "My card numbers are 3aeedea8fef2 and 3b49ffea0e53. Invalid: 4111 1111 1111 1112."
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)
