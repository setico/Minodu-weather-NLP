from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate" # URL par défaut d'Ollama
OLLAMA_MODEL = "gemma3:4b" # Le modèle Ollama

@app.route('/weather-interpretation', methods=['POST'])
def weather_interpretation():
    data = request.json

    if not data:
        return jsonify({"error": "Aucune donnée JSON fournie"}), 400

    # Extraction des données brutes
    temp = data.get("temp")
    hum = data.get("hum")
    hum1 = data.get("hum1")
    temp1 = data.get("temp1")
    press = data.get("press")
    alt = data.get("alt")
    lux = data.get("lux")
    ambient = data.get("ambient")
    co = data.get("CO")
    no2 = data.get("NO2")

    # Déterminer la saison
    # A kara, La saison sèche s'étend généralement de novembre à mars, tandis que la saison des pluies s'étend d'avril à octobre
    current_month = datetime.now().month
    if 4 <= current_month <= 10:
        saison = "saison des pluies"
    else:
        saison = "saison sèche"

    # Construction du prompt
    prompt = f"""
    Agis en tant qu'expert en météorologie. Analyse et interprète les données brutes d'une station météo de Kara, au nord du Togo, pour des agriculteurs.
    Les données brutes sont les suivantes :
    Température actuelle (capteur 1): {temp}°C
    Humidité relative (capteur 1): {hum}%
    Température actuelle (capteur 2): {temp1}°C
    Humidité relative (capteur 2): {hum1}%
    Pression atmosphérique: {press} hPa
    Altitude relative (calculée): {alt} mètres
    Luminosité: {lux} lux
    Luminosité ambiante: {ambient}
    Monoxyde de carbone (CO): {co}
    Dioxyde d'azote (NO2): {no2}
    Saison actuelle (basée sur la date d'aujourd'hui): {saison}

    Fournis en un seul paragraphe en français simple exposant les conditions météo actuelles, les prévisions de pluie (si pertinentes), les informations sur la pollution (si disponibles), et les implications pour les plantes et les cultures. Tiens compte de la saison actuelle lors de ton analyse.
    """

    # Appel à l'API Ollama
    try:
        ollama_response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False # Pour obtenir la réponse complète en une seule fois
            }
        )
        ollama_response.raise_for_status()
        response_data = ollama_response.json()
        generated_text = response_data.get("response", "Aucune réponse générée par Ollama.")

        return jsonify({"weather_interpretation": generated_text}), 200

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Impossible de se connecter à Ollama. Assurez-vous qu'Ollama est en cours d'exécution et que le modèle est chargé."}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erreur lors de l'appel à l'API Ollama: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)