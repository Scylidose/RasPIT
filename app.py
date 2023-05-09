from flask import Flask, request, jsonify
from speech.speech_to_text import transcribe_audio_file
from speech.text_to_speech import synthesize_speech
from gpt.client import generate_response
from remote_actions.action_handler import execute_remote_action
import os

app = Flask(__name__)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    if not os.path.exists('temp'):
        os.makedirs('temp')

    audio_file = request.files['audio_file']
    file_path = os.path.join('temp', 'input.wav')
    audio_file.save(file_path)

    # Convert speech to text
    user_text = transcribe_audio_file(file_path)

    # Process the text input with GPT-3
    gpt3_response = generate_response(user_text)

    # Check for remote actions
    remote_action_result = execute_remote_action(gpt3_response)
    if remote_action_result:
        gpt3_response = f"Action executed: {gpt3_response}"

    # Convert text response to speech
    audio_response = synthesize_speech(gpt3_response)

    with open('temp/output.mp3', 'wb') as f:
        f.write(audio_response)

    return jsonify({'response_text': gpt3_response, 'response_audio': 'temp/output.mp3'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
