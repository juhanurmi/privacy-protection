import pytest
from unittest.mock import patch
from privacy_protection import protect_privacy

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_locations(mock_write, mock_read):
    """Test the protect_privacy function."""
    mock_read.return_value = "Lappland is in Finland. San Francisco is in California, USA."
    protect_privacy("dummy.txt")
    expected_output = (
        "location-3958cda14415 is in location-b2dd18316d3c. location-84dff33fb867 is in location-5f09fa0934d4, location-b52e5b605c5f."
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)
