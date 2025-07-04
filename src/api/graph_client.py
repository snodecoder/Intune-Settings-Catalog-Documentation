class GraphClient:
    def __init__(self, client_id, client_secret, tenant_id):
        self.client_id = os.getenv("CLIENT_ID", client_id)
        self.client_secret = os.getenv("CLIENT_SECRET", client_secret)
        self.tenant_id = os.getenv("TENANT_ID", tenant_id)
        self.token = self.authenticate()

    def authenticate(self):
        import requests
import os

        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default"
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")

    def get_setting_definitions(self):
        url = "https://graph.microsoft.com/beta/deviceManagement/settingDefinitions"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_configuration_settings(self):
        url = "https://graph.microsoft.com/beta/deviceManagement/configurationSettings"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
