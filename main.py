from flask import Flask, render_template, request, redirect
import speech_recognition as sr

# from HarborviewProject.model import db


app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/languages")
def languages():
    return render_template("languages.html")


@app.route("/stt", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, language="fr-FR", key=None)
            #print(transcript)

    return render_template('index.html', transcript=transcript)

#@app.route("/stt1", methods=["GET", "POST"])
# Google
def transcribe_file_with_multilanguage():
    """Transcribe the given audio file synchronously with
    multi language."""
    # [START speech_transcribe_multilanguage_beta]
    from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()

    speech_file = "static/french1.wav"
    first_lang = "fr-FR"
    second_lang = "es-ES"

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        audio_channel_count=2,
        language_code=first_lang,
        alternative_language_codes=[second_lang],
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(u"First alternative of result {}: {}".format(i, alternative))
        print(u"Transcript: {}".format(alternative.transcript))
    # [END speech_transcribe_multilanguage_beta]


# @app.route("/card/<int: index>")
# def card_view(index):
#     card = db[index]
#     return render_template("card.html", card=card)
