from collections import defaultdict
import json

def load_settings():
    with open('settingDefinitions.json') as f:
        setting_definitions = json.load(f)
    
    with open('configurationSettings.json') as f:
        configuration_settings = json.load(f)
    
    return setting_definitions, configuration_settings

def process_settings(setting_definitions, configuration_settings):
    processed_data = defaultdict(list)

    for setting in setting_definitions.get('value', []):
        category = setting.get('category', 'Uncategorized')
        processed_data[category].append({
            'id': setting.get('id'),
            'name': setting.get('displayName'),
            'description': setting.get('description'),
            'value': None  # Placeholder for value from configuration settings
        })

    for config in configuration_settings.get('value', []):
        for setting in processed_data.get(config.get('category', 'Uncategorized'), []):
            if setting['id'] == config.get('id'):
                setting['value'] = config.get('value')

    return processed_data

def filter_settings(processed_data, search_term):
    filtered_data = {}
    for category, settings in processed_data.items():
        filtered_settings = [s for s in settings if search_term.lower() in s['name'].lower() or search_term.lower() in s['description'].lower()]
        if filtered_settings:
            filtered_data[category] = filtered_settings
    return filtered_data

def group_settings_by_category(processed_data):
    return dict(processed_data)  # Already grouped by category

def main():
    setting_definitions, configuration_settings = load_settings()
    processed_data = process_settings(setting_definitions, configuration_settings)
    return processed_data

if __name__ == "__main__":
    main()