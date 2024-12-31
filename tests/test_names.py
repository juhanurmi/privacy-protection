import pytest
from unittest.mock import patch
from privacy_protection import protect_privacy

@patch("privacy_protection.read_file")
@patch("privacy_protection.write_file")
@patch("privacy_protection.RANDOM_SALT", new="abc123")
def test_names(mock_write, mock_read):
    """Test the protect_privacy function."""
    mock_read.return_value = "Juha Nurmi, Constantinos, David, Sara, Arttu Paju, ..."
    protect_privacy("dummy.txt")
    expected_output = (
        "name-3d5714dd49a9, name-ef7e2d889513, name-2d7675ba0a9c, Sara, name-3dd9550407f4, ..."
    )
    mock_write.assert_called_once_with("dummy.txt.protected", expected_output)
