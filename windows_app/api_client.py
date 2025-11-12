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
            return True, None
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            return False, str(e)

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

    def get_all_items(self, endpoint: str):
        try:
            headers = self._get_auth_headers()
            response = requests.get(f"{self.base_url}/{endpoint}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get items from {endpoint}: {e}")
            return None

    def _get_public_items(self, endpoint: str):
        try:
            response = requests.get(f"{self.base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get public items from {endpoint}: {e}")
            return None

    def get_item(self, endpoint: str, item_id: int):
        try:
            headers = self._get_auth_headers()
            response = requests.get(f"{self.base_url}/{endpoint}/{item_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get item {item_id} from {endpoint}: {e}")
            return None

    def create_item(self, endpoint: str, data: dict):
        try:
            headers = self._get_auth_headers()
            response = requests.post(f"{self.base_url}/{endpoint}", json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to create item in {endpoint}: {e}")
            return None

    def update_item(self, endpoint: str, item_id: int, data: dict):
        try:
            headers = self._get_auth_headers()
            response = requests.put(f"{self.base_url}/{endpoint}/{item_id}", json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to update item {item_id} in {endpoint}: {e}")
            return None

    def delete_item(self, endpoint: str, item_id: int):
        try:
            headers = self._get_auth_headers()
            response = requests.delete(f"{self.base_url}/{endpoint}/{item_id}", headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to delete item {item_id} from {endpoint}: {e}")
            return False

    def get_sedes(self):
        return self._get_public_items("sedes")

    def get_categorias(self):
        return self._get_public_items("categorias")

    def get_estados(self):
        return self._get_public_items("estados")

    def get_marcas(self):
        return self._get_public_items("marcas")

    def get_modelos(self):
        return self._get_public_items("modelos")

    def get_procesos(self):
        return self._get_public_items("procesos")

    def get_responsables(self):
        return self._get_public_items("responsables")

    def get_ubicaciones(self):
        return self._get_public_items("ubicaciones")

    def get_host(self, host_id):
        try:
            headers = self._get_auth_headers()
            response = requests.get(f"{self.base_url}/hosts/{host_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get host {host_id}: {e}")
            return None

    def get_monitoreo_by_host(self, host_id, start_date=None, end_date=None):
        try:
            headers = self._get_auth_headers()
            params = {}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date

            response = requests.get(f"{self.base_url}/monitoreo/{host_id}", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get monitoreo data for host {host_id}: {e}")
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
        print(f"Updating host {host_id} with data: {host_data}")
        try:
            headers = self._get_auth_headers()
            response = requests.put(f"{self.base_url}/hosts/{host_id}", json=host_data, headers=headers)
            print(f"Update response status code: {response.status_code}")
            print(f"Update response content: {response.text}")
            response.raise_for_status()
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Failed to update host: {e}")
            return False

    def delete_host(self, host_id):
        print(f"Deleting host {host_id}")
        try:
            headers = self._get_auth_headers()
            response = requests.delete(f"{self.base_url}/hosts/{host_id}", headers=headers)
            print(f"Delete response status code: {response.status_code}")
            print(f"Delete response content: {response.text}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to delete host: {e}")
            return False

    def submit_monitoreo_result(self, host_id, data):
        try:
            headers = self._get_auth_headers()
            response = requests.post(f"{self.base_url}/monitoreo/{host_id}", json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to submit monitoreo result for host {host_id}: {e}")
            return None
