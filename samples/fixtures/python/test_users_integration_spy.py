import unittest
from datetime import datetime
from unittest.mock import patch
import requests
from users import get_users, User

LOG_FILE = "spy-http-calls.log"

class TestGetUsersIntegrationWithSpy(unittest.TestCase):
    def test_get_users_and_log_http_calls(self):
        original_get = requests.get

        def get_spy(*args, **kwargs):
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(
                    f"{datetime.now().isoformat()} "
                    f"requests.get args={args} kwargs={kwargs}\n"
                )
            return original_get(*args, **kwargs)

        with patch("users.requests.get", side_effect=get_spy) as spy_get:
            users = get_users()

        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], User)
        spy_get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/users",
            timeout=5
        )

if __name__ == "__main__":
    unittest.main()
