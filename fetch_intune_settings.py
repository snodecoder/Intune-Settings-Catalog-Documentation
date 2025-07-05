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


    # Build lookup maps for categories and definitions
    def_map = {d.get("id"): d for d in setting_defs if "id" in d}
    cat_map = {c["id"]: c for c in categories if "id" in c}
    root_cat_map = {c["id"]: c["displayName"] for c in categories if "id" in c and "displayName" in c}

    # Collect all platforms, categories, and keywords
    platforms_set = set()
    categories_set = set()
    keywords_set = set()
    platform_settings = {}
    platform_indexes = {}

    for s in config_settings:
        # Find the setting definition by id (if available)
        setting_def = def_map.get(s.get("settingDefinitionId")) if s.get("settingDefinitionId") else None
        # Find the category and root category
        cat = cat_map.get(s.get("categoryId"))
        root_id = cat["rootCategoryId"] if cat and "rootCategoryId" in cat else None
        root_name = root_cat_map.get(root_id, "Uncategorized")
        # Get platform(s) from category
        platforms = cat.get("platforms", "Unknown").split(",") if cat else ["Unknown"]
        platforms = [p.strip().lower() for p in platforms if p.strip()]
        for p in platforms:
            platforms_set.add(p)
        categories_set.add(root_name)
        for kw in s.get("keywords", []):
            keywords_set.add(kw)
        # Merge all relevant properties from the configuration setting
        item = {
            "settingId": s.get("id"),
            "settingName": s.get("displayName"),
            "settingDescription": s.get("description"),
            "categoryId": s.get("categoryId"),
            "categoryName": root_name,
            "keywords": s.get("keywords", []),
            "baseUri": s.get("baseUri"),
            "offsetUri": s.get("offsetUri"),
            "settingUsage": s.get("settingUsage"),
            "uxBehavior": s.get("uxBehavior"),
            "visibility": s.get("visibility"),
            "riskLevel": s.get("riskLevel"),
            "defaultOptionId": s.get("defaultOptionId"),
            "applicability": s.get("applicability"),
            "options": s.get("options", []),
            "referredSettingInformationList": s.get("referredSettingInformationList", []),
            "accessTypes": s.get("accessTypes"),
            "version": s.get("version"),
            "helpText": s.get("helpText"),
            "name": s.get("name"),
            "rootDefinitionId": s.get("rootDefinitionId"),
            # Supplement with definition fields if available
            "settingDefinitionId": s.get("settingDefinitionId"),
            "definitionDescription": setting_def.get("description") if setting_def else None,
            "dataType": setting_def.get("dataType") if setting_def else s.get("dataType"),
            "valueOptions": setting_def.get("options") if setting_def and "options" in setting_def else s.get("options", []),
            "dependencies": setting_def.get("dependencies") if setting_def and "dependencies" in setting_def else s.get("dependencies", []),
        }
        # Add to each platform's list
        for p in platforms:
            if p not in platform_settings:
                platform_settings[p] = []
            platform_settings[p].append(item)

    # Write per-platform settings files and search indexes
    for p, items in platform_settings.items():
        fname = f"{p}.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        # Create a search index (id, name, description, keywords, categoryName)
        index = [
            {
                "settingId": i["settingId"],
                "settingName": i["settingName"],
                "settingDescription": i["settingDescription"],
                "keywords": i["keywords"],
                "categoryName": i["categoryName"]
            }
            for i in items
        ]
        with open(f"{p}_index.json", "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    # Write metadata files
    with open("platforms.json", "w", encoding="utf-8") as f:
        json.dump(sorted(list(platforms_set)), f, indent=2, ensure_ascii=False)
    with open("categories.json", "w", encoding="utf-8") as f:
        json.dump(sorted(list(categories_set)), f, indent=2, ensure_ascii=False)
    with open("keywords.json", "w", encoding="utf-8") as f:
        json.dump(sorted(list(keywords_set)), f, indent=2, ensure_ascii=False)

    # Optionally, remove the old intune_settings.json
    # if os.path.exists("intune_settings.json"):
    #     os.remove("intune_settings.json")

if __name__ == "__main__":
    main()
