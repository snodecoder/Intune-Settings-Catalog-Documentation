# Intune Settings Overview

This project provides an overview of Microsoft Intune settings by connecting to the Microsoft Graph API. It retrieves data from the `settingDefinitions` and `configurationSettings` endpoints, processes the data, and presents it in a user-friendly web application.

## Project Structure

```
intune-settings-overview
├── src
│   ├── api
│   │   ├── graph_client.py       # Handles authentication and API communication
│   │   └── __init__.py           # Initializes the api module
│   ├── data
│   │   ├── fetch_settings.py      # Fetches data from the Graph API
│   │   ├── process_settings.py     # Processes and filters the settings data
│   │   └── __init__.py           # Initializes the data module
│   ├── web
│   │   ├── app.py                 # Entry point for the web application
│   │   ├── templates
│   │   │   └── index.html         # Main HTML template for displaying settings
│   │   ├── static
│   │   │   ├── style.css          # CSS styles for the web application
│   │   │   └── script.js          # JavaScript for client-side interactivity
│   │   └── __init__.py           # Initializes the web module
│   └── utils
│       └── __init__.py           # Initializes the utils module
├── settingDefinitions.json         # Stores retrieved setting definitions
├── configurationSettings.json       # Stores retrieved configuration settings
├── requirements.txt                # Lists project dependencies
└── README.md                       # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd intune-settings-overview
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Configure Microsoft Graph API**:
   - Register your application in the Azure portal.
   - Obtain the necessary credentials (Client ID, Tenant ID, Client Secret).
   - Update the `graph_client.py` file with your credentials.

4. **Run the application**:
   ```
   python src/web/app.py
   ```

5. **Access the web application**:
   Open your web browser and navigate to `http://localhost:5000` to view the Intune settings overview.

## Functionality

- **Data Retrieval**: The application fetches settings data from the Microsoft Graph API and stores it in JSON files.
- **Data Processing**: The settings data is processed to allow filtering and grouping by root category.
- **Web Interface**: A simple web interface displays the settings, their values, and descriptions, with search and filter capabilities.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.