import unittest
from unittest.mock import patch, Mock
from users import get_users, User

class TestGetUsers(unittest.TestCase):
    @patch("users.requests.get")
    def test_get_users(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "Leanne Graham", "username": "Bret", "email": "Sincere@april.biz"},
            {"id": 2, "name": "Ervin Howell", "username": "Antonette", "email": "Shanna@melissa.tv"}
        ]
        mock_get.return_value = mock_response

        users = get_users()

        self.assertEqual(2, len(users))
        self.assertIsInstance(users[0], User)
        self.assertEqual(1, users[0].id)
        self.assertEqual("Leanne Graham", users[0].name)
        self.assertEqual("Bret", users[0].username)
        mock_get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/users",
            timeout=5
        )
        mock_response.raise_for_status.assert_called_once()

if __name__ == "__main__":
    unittest.main()
