import unittest
from users import get_users, User

class TestGetUsersIntegration(unittest.TestCase):
    def test_get_users_from_api(self):
        users = get_users()

        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], User)
        self.assertIsInstance(users[0].id, int)
        self.assertIsInstance(users[0].name, str)
        self.assertIsInstance(users[0].username, str)
        self.assertIsInstance(users[0].email, str)

if __name__ == "__main__":
    unittest.main()
