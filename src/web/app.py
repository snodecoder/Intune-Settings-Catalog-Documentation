from flask import Flask, render_template, request, jsonify
import json
from src.data.process_settings import process_setting_definitions, process_configuration_settings

app = Flask(__name__)

@app.route('/')
def index():
    with open('../settingDefinitions.json') as f:
        setting_definitions = json.load(f)
    with open('../configurationSettings.json') as f:
        configuration_settings = json.load(f)

    processed_settings = process_setting_definitions(setting_definitions)
    processed_configuration = process_configuration_settings(configuration_settings)

    return render_template('index.html', settings=processed_settings, configuration=processed_configuration)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    with open('../settingDefinitions.json') as f:
        setting_definitions = json.load(f)

    filtered_settings = [setting for setting in setting_definitions['value'] if query.lower() in setting.get('description', '').lower()]

    return jsonify(filtered_settings)

if __name__ == '__main__':
    app.run(debug=True)