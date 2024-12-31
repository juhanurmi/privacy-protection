import pytest
from unittest.mock import patch
from privacy_protection import protect_privacy

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_names(mock_write, mock_read):
    """Test the protect_privacy function."""
    mock_read.return_value = "Juha Nurmi, Constantinos Patsakis, David Arroyo, ..."
    protect_privacy("dummy.txt")
    expected_output = (
        "name-3d5714dd49a9, name-af30a186d1ea, name-f07b2f46c449, ..."
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)
