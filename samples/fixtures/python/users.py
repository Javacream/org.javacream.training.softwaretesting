from dataclasses import dataclass
import requests

DEFAULT_USERS_URL = "https://jsonplaceholder.typicode.com/users"

@dataclass
class User:
    id: int
    name: str
    username: str
    email: str

def get_users(url: str = DEFAULT_USERS_URL) -> list[User]:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return [
        User(id=u["id"], name=u["name"], username=u["username"], email=u["email"])
        for u in response.json()
    ]
