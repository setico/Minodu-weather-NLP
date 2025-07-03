# NLP weather API for the Minodu LCN

This project provides a lightweight Flask API deployed on a Raspberry Pi, designed to deliver interpreted weather bulletins specifically for the teleagriculture stations deployed in the farmers communities in Kara, northern Togo. The API uses a local language model (LLM) via Ollama to analyze raw weather station data and generate relevant forecasts and advice for agriculture, taking into account the current season.

## Features

- **Contextualized weather analysis**: Interprets data on temperature, humidity, pressure, luminosity, and pollution.
- **Specific agricultural advice**: Provides direct implications for plants and crops, adapted to local conditions.
- **Seasonal consideration**: Adjusts the analysis based on Kara's rainy or dry season.
- **Local deployment**: Uses Ollama and a local LLM (gemma3:4b) for offline data processing.
- **Simple API interface**: Easy to integrate with other systems or applications.

## Prerequisites

To deploy and run this project, you will need:
- A Raspberry Pi (or any other compatible Linux system).
- Ollama installed on your Raspberry Pi.
- An Ollama-compatible language model (e.g., gemma3:4b) downloaded.
- Python 3 and pip.

## Installation and configuration

Follow these steps to set up and launch the API on your Raspberry Pi.

### 1. Ollama configuration on Raspberry Pi

Connect to your Raspberry Pi via SSH and run the following commands:

```bash
# Update system packages
sudo apt-get update

# Install curl (if not already installed)
sudo apt-get install curl

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify Ollama installation
ollama --version
```
### 2. Language model download

Download the gemma3:4b model (or another model of your choice) via Ollama. This model will be used by the API for weather interpretation.

```bash
ollama run gemma3:4b
```
Allow the download to complete. You can exit the model prompt after downloading by typing Ctrl+D.

### 3. API file upload (app.py)

From your local machine, use scp to transfer the app.py file to your Raspberry Pi. Replace 10.0.0.115 with your Raspberry Pi's IP address and /path/to/local/app.py with the local path to your app.py file.

```bash
scp /path/to/local/app.py pi@10.0.0.115:/home/pi/
```

### 4. Python environment configuration on Raspberry Pi

On your Raspberry Pi, set up a virtual environment to isolate project dependencies:

```bash
# Install pip (if not already installed)
sudo apt-get install python3-pip

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies (Flask and requests)
pip install Flask requests
```

### 5. Launching the API server

Once the virtual environment is activated, you can launch the Flask application:

```bash
# Ensure the virtual environment is activated (you should see (venv) in your command prompt)
source venv/bin/activate

# Execute the Flask application
python app.py
```
The server will be accessible at http://<raspberry_pi_ip_address>:5000/.

### API usage

The API exposes a POST endpoint to receive weather station data and return the interpretation.

Endpoint: /weather-interpretation<br>
Method: POST<br>
Content-Type: application/json<br>

**Example request**<br>
You can test the API using curl from another machine on the same network as your Raspberry Pi. Replace 10.0.0.115 with your Raspberry Pi's IP address.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"Battery":0,"temp":22,"hum":27,"hum1":29.02000046,"temp1":21.51000023,"press":1013.599976,"alt":-2.920000076,"lux":74.80000305,"ambient":161,"CO":0,"NO2":9558}' http://10.0.0.115:5000/weather-interpretation
```

**Example response**

```bash
{
"weather_interpretation": "Mesdames et Messieurs les agriculteurs, voici l'analyse de la météo à Kara, au Togo, pour vous aider à prendre vos décisions. Actuellement, nous avons une température de 22°C et une humidité relative de 27%, ce qui est relativement confortable pour les cultures. Étant donné que nous sommes en plein cœur de la saison des pluies, les conditions sont favorables à la croissance, avec une humidité qui favorisera l’absorption d'eau par les plantes. La pression atmosphérique est normale (1013.5 hPa), et l’altitude de 2 mètres n’est pas un facteur important dans ce contexte. La luminosité à 74 lux est suffisante pour la photosynthèse, bien que nous recommandions de surveiller cette valeur avec le passage des nuages. Bien qu'il y ait une présence de NO2 à 9558, cette valeur est élevée et peut provenir de sources locales, mais n'affecte pas directement les cultures. En résumé, cette journée est idéale pour la plupart des cultures, particulièrement celles qui ont besoin d'une humidité élevée. Continuez à surveiller les prévisions des pluies – elles restent probables dans cette saison – et assurez-vous que vos cultures sont bien drainées pour éviter les maladies liées à l'excès d'humidité."
}
```

### Technologies Used
- Python 3
- Flask: Web micro-framework for the API.
- Ollama: For local execution of language models.
- Gemma 3:4b: Language model used for interpretation.
- Raspberry Pi OS: Operating system of the deployment device.