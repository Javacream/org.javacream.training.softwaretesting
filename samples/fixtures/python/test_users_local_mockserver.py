import unittest
from users import get_users, User

MOCKSERVER_URL = "http://localhost:1080/users"

class TestGetUsersLocalMockServer(unittest.TestCase):
    def test_get_users_from_local_mockserver(self):
        users = get_users(MOCKSERVER_URL)

        self.assertEqual(2, len(users))
        self.assertIsInstance(users[0], User)
        self.assertEqual(201, users[0].id)
        self.assertEqual("Local Mock User One", users[0].name)
        self.assertEqual("localuser1", users[0].username)
        self.assertEqual("local1@test.example", users[0].email)

        self.assertEqual(202, users[1].id)
        self.assertEqual("Local Mock User Two", users[1].name)

if __name__ == "__main__":
    unittest.main()
