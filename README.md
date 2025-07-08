# Intune Settings Catalog Documentation

This project fetches, processes, and publishes the Microsoft Intune Settings Catalog data. It provides a searchable, filterable web interface for exploring Intune configuration settings, categories, and keywords.

## What does it do?
- Uses Microsoft Graph API to download the latest Intune configuration settings, definitions, and categories.
- Processes and organizes the data by platform, category, and keyword.
- Generates static JSON files and a web interface for easy browsing.
- Publishes the results as a GitHub Pages site.

## How to use the GitHub Pages site
Visit: [https://snodecoder.github.io/Intune-Settings-Catalog-Documentation/](https://snodecoder.github.io/Intune-Settings-Catalog-Documentation/)

- **Filter by platform, category, or keyword** using the dropdowns at the top.
- **Search for settings** by name or description using the search box.
- **Browse results** in a paginated table. Click "Show details" for more information about each setting.
- The site is updated automatically with the latest data from Microsoft Graph.
- **The GitHub Pages site is refreshed with the latest Intune data every week on Sunday night.**

![image](https://github.com/user-attachments/assets/47de35d3-ae85-4b67-845e-654655617279)

## Contributing
Contributions are welcome! If you find a bug, have a suggestion, or want to improve this project, please open an issue or submit a pull request. Your input helps make this project better for everyone. Thank you for your support!


## Local development
- Run `fetch_intune_settings.py` to fetch and update the data (requires Azure credentials).
- The static site is generated in the `website_data` folder and served via `index.html`.

## License
This project is provided as-is for documentation and research purposes.
