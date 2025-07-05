import os
import json
import requests
import msal

def get_access_token():
    tenant_id = os.environ['TENANT_ID']
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scope = ["https://graph.microsoft.com/.default"]

    app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
    result = app.acquire_token_for_client(scopes=scope)
    if "access_token" not in result:
        raise Exception("Failed to get token: " + json.dumps(result, indent=2))
    return result["access_token"]

def fetch_graph_data(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    data = []
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        result = r.json()
        data.extend(result.get("value", []))
        url = result.get("@odata.nextLink")
    return data

def main():
    token = get_access_token()

    config_settings = fetch_graph_data("https://graph.microsoft.com/beta/deviceManagement/configurationSettings", token)
    print(f"Fetched {len(config_settings)} configuration settings.")

    setting_defs = fetch_graph_data("https://graph.microsoft.com/beta/deviceManagement/settingDefinitions", token)
    print(f"Fetched {len(setting_defs)} setting definitions.")

    categories = fetch_graph_data("https://graph.microsoft.com/beta/deviceManagement/configurationCategories", token)
    print(f"Fetched {len(categories)} configuration categories.")
    with open("configurationSettings.json", "w", encoding="utf-8") as f:
        json.dump(config_settings, f, indent=2, ensure_ascii=False)

    with open("settingDefinitions.json", "w", encoding="utf-8") as f:
        json.dump(setting_defs, f, indent=2, ensure_ascii=False)

    with open("configurationCategories.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)


    def_map = {d["settingInstanceTemplateId"]: d for d in setting_defs if "settingInstanceTemplateId" in d}
    cat_map = {c["id"]: c.get("rootCategoryId", c["id"]) for c in categories}
    root_cat_map = {c["id"]: c["displayName"] for c in categories}

    grouped = {}
    for s in config_settings:
        template_id = s.get("settingInstanceTemplateId")
        d = def_map.get(template_id, {})
        root_id = cat_map.get(s.get("categoryId"), "Uncategorized")
        root_name = root_cat_map.get(root_id, "Uncategorized")

        item = {
            "name": s.get("settingName"),
            "description": d.get("description"),
            "dataType": d.get("dataType"),
            "valueOptions": d.get("options", []),
            "settingValueTemplateId": template_id
        }
        grouped.setdefault(root_name, []).append(item)

    with open("intune_settings.json", "w", encoding="utf-8") as f:
        json.dump(grouped, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
