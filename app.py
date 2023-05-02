from flask import Flask, request, jsonify
from speech import speech_to_text, text_to_speech
from gpt import client
from remote_actions import action_handler

app = Flask(__name__)

@app.route("/speech_to_text", methods=["POST"])
def process_speech():
    return 0

@app.route("/text_to_speech", methods=["POST"])
def synthesize_speech():
    return 0

@app.route("/process_text", methods=["POST"])
def process_text():
    return 0

@app.route("/execute_action", methods=["POST"])
def execute_action():
    return 0

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
