import json
from api.graph_client import GraphClient

def fetch_and_save_settings():
    client = GraphClient()

    # Fetch setting definitions
    setting_definitions = client.get_setting_definitions()
    with open('settingDefinitions.json', 'w') as f:
        json.dump(setting_definitions, f)

    # Fetch configuration settings
    configuration_settings = client.get_configuration_settings()
    with open('configurationSettings.json', 'w') as f:
        json.dump(configuration_settings, f)

if __name__ == "__main__":
    fetch_and_save_settings()