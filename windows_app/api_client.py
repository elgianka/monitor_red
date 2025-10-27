import requests

class ApiClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api/v1"):
        self.base_url = base_url
        self.token = None

    def authenticate(self, username, password):
        try:
            response = requests.post(f"{self.base_url}/token", data={"username": username, "password": password})
            response.raise_for_status()
            self.token = response.json().get("access_token")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            return False

    def _get_auth_headers(self):
        if not self.token:
            raise Exception("Not authenticated. Please call authenticate() first.")
        return {"Authorization": f"Bearer {self.token}"}

    def get_hosts(self):
        try:
            headers = self._get_auth_headers()
            response = requests.get(f"{self.base_url}/hosts", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get hosts: {e}")
            return None

    def get_active_alerts(self):
        try:
            headers = self._get_auth_headers()
            response = requests.get(f"{self.base_url}/alerts/active", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get active alerts: {e}")
            return None

    def create_host(self, host_data):
        try:
            headers = self._get_auth_headers()
            response = requests.post(f"{self.base_url}/hosts", json=host_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to create host: {e}")
            return None

    def update_host(self, host_id, host_data):
        try:
            headers = self._get_auth_headers()
            response = requests.put(f"{self.base_url}/hosts/{host_id}", json=host_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to update host: {e}")
            return None

    def delete_host(self, host_id):
        try:
            headers = self._get_auth_headers()
            response = requests.delete(f"{self.base_url}/hosts/{host_id}", headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to delete host: {e}")
            return False
