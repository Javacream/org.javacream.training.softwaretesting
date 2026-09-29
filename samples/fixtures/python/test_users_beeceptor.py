import unittest
from users import get_users, User

# Durch die tatsächlich bei Beeceptor angelegte URL ersetzen.
BEECEPTOR_URL = "https://softwaretesting-users.free.beeceptor.com/users"

class TestGetUsersBeeceptor(unittest.TestCase):
    def test_get_users_from_beeceptor(self):
        users = get_users(BEECEPTOR_URL)

        self.assertEqual(2, len(users))
        self.assertIsInstance(users[0], User)
        self.assertEqual(101, users[0].id)
        self.assertEqual("Test User One", users[0].name)
        self.assertEqual("testuser1", users[0].username)
        self.assertEqual("user1@test.example", users[0].email)

if __name__ == "__main__":
    unittest.main()
