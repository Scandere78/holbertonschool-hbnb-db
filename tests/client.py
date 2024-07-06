import requests

from tests import API_URL, PASSWORD_USER
from tests import auth_headers


class ClientUser:
    data: dict
    id: str
    is_admin: bool
    access_token: str

    def __init__(self, data: dict, access_token: str, is_admin: bool):
        self.data = data
        self.id = data['id']
        self.access_token = access_token
        self.is_admin = is_admin


class Client:
    superuser: ClientUser
    user: ClientUser
    user2: ClientUser

    def __init__(self):
        print("> Client for tests initialization...")
        from tests.factory import Factory

        self.factory = Factory(self)

        superuser = self.factory.create_unique_user(True)
        access_token = self.login(superuser)
        self.superuser = ClientUser(superuser, access_token, True)

        user = self.factory.create_unique_user(False)
        access_token = self.login(user)
        self.user = ClientUser(user, access_token, False)

        user2 = self.factory.create_unique_user(False)
        access_token = self.login(user2)
        self.user2 = ClientUser(user2, access_token, False)
        print("> Client for tests initialization: OK!")

    def get(self, path: str, access_token = None) -> requests.Response:
        return requests.get(
            f"{API_URL}{path}",
            headers= {} if not access_token else auth_headers(access_token)
        )

    def post(self, path: str, data: dict, access_token = None) -> requests.Response:
        return requests.post(
            f"{API_URL}{path}",
            json=data,
            headers= {} if not access_token else auth_headers(access_token)
        )

    def put(self, path: str, data: dict, access_token = None) -> requests.Response:
        return requests.put(
            f"{API_URL}{path}",
            json=data,
            headers= {} if not access_token else auth_headers(access_token)
        )

    def delete(self, path: str, access_token = None) -> requests.Response:
        return requests.delete(
            f"{API_URL}{path}",
            headers= {} if not access_token else auth_headers(access_token)
        )

    def login(self, user: dict, force_password = None):
        """
            Helper function to login a user.
        """
        # Login
        response_login = requests.post(f"{API_URL}/login", json={
            "email": user['email'],
            "password": force_password if force_password else PASSWORD_USER
        })
        assert (
            response_login.status_code == 201
        ), f"Expected status code 201 but got {response_login.status_code}. Response: {response_login.text}"

        return response_login.json()["access_token"]
