import requests

class CRMClient:
    def __init__(self, base_url: str, access_token: str, id_token: str):
        if not base_url:
            raise ValueError("BASE_URL is not set")
        if not access_token:
            raise ValueError("AUTH_ACCESS_TOKEN is not set")
        if not id_token:
            raise ValueError("AUTH_ID_TOKEN is not set")

        self.base_url = base_url.rstrip("/")

        self.headers = {
            "AccessToken": access_token,
            "IdToken": id_token,
            "Content-Type": "application/json",
        }

    def get_operations(self):
        url = f"{self.base_url}/operations"
        return requests.get(url, headers=self.headers)

    def get_waiters_management(self):
        url = f"{self.base_url}/employees"
        return requests.get(url, headers=self.headers)

    def get_clients(self):
        url = f"{self.base_url}/clients"
        return requests.get(url, headers=self.headers)