from flask import Flask, render_template, request
import azure.cognitiveservices.speech as speechsdk
import requests
import json, uuid

app = Flask(__name__)

# Replace with your own endpoint and subscription key for Translator Text API
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/"
TRANSLATOR_SUBSCRIPTION_KEY = "d08b3ea83ed84663be2ed4c141fecb5a"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    # Get the speech-to-text language from the form data
    stt_language = request.form["stt_language"]

    # Create a speech recognizer
    speech_config = speechsdk.SpeechConfig(subscription="15e9740350164db6965aeca7b73d49d7", region="centralindia")
    speech_config.speech_recognition_language = stt_language
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    # Start the speech recognizer and wait for a result
    result = speech_recognizer.recognize_once_async().get()

    # Get the text from the speech-to-text result
    text = result.text

    # Translate the text to the desired language using the Translator Text API
    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_SUBSCRIPTION_KEY,
        "Ocp-Apim-Subscription-Region": "centralindia",
        "Content-Type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }

    body = [{
        "text": text
    }]
    target_language= request.form["translation_language"]
    params = "&to=" + target_language
    constructed_url = TRANSLATOR_ENDPOINT + "/translate?api-version=3.0" + params

    response = requests.post(constructed_url, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()
    translation = result[0]["translations"][0]["text"]

    return render_template("result.html", text=text, translation=translation)
