import pytest
from unittest.mock import patch
from privacy_protection import protect_privacy

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_ipv6(mock_write, mock_read):
    """Test the protect_privacy function."""
    mock_read.return_value = '''2266:0025:0:0:0:0012:0000:ad12
        2266:0025::0012:0000:ad12
        2266:25:0:0:0:12:0000:ad12
        2266:25:0:0:0:12:0:ad12
        2266:25::12:0:ad12
        2266:25::12::ad12'''
    protect_privacy("dummy.txt")
    expected_output = (
        '''ipv6-c6d19508c6af
        2266:0025::0012:0000:ad12
        ipv6-10c8cf4f89ec
        ipv6-864ff4f6d642
        2266:25::12:0:ad12
        2266:25::12::ad12'''
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)
