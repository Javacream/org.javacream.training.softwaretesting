import unittest
from unittest.mock import Mock

from users import get_users, User


LOG_FILE = "spy-calls.log"


def create_spy(function, logfile):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)

        with open(logfile, "a", encoding="utf-8") as log:
            log.write(f"Function: {function.__name__}\n")
            log.write(f"Args: {args}\n")
            log.write(f"Kwargs: {kwargs}\n")
            log.write(f"Return value: {result}\n")
            log.write("\n")

        return result

    return Mock(side_effect=wrapper)


class TestGetUsersWithSpy(unittest.TestCase):

    def test_get_users_with_spy(self):
        spy = create_spy(get_users, LOG_FILE)

        users = spy()

        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], User)

        spy.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
