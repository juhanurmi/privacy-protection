import pytest
from unittest.mock import patch
from privacy_protection import protect_privacy

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_ipv4(mock_write, mock_read):
    """Test the protect_privacy function."""
    mock_read.return_value = "Private 10.0.0.0/8 and 172.16.0.0/12 and 192.168.0.0/16. 46.19.38.63. 8.8.8.8."
    protect_privacy("dummy.txt")
    expected_output = (
        "Private 10.0.0.0/8 and 172.16.0.0/12 and 192.168.0.0/16. ipv4-8e8df7ce. 8.8.8.8."
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)
