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
