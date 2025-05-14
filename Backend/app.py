import os
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from midi import create_midi, midi_to_wav

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.shapes.inc/v1/"  # Replace with the actual endpoint

def generate_music_prompt(scale="C_major", length=16):
    prompt = (

        f"Generate a melody in the {scale} scale with {length} notes. "
        f"Make sure the notes include octaves and can include sharps or flats. "
        f"Respond in the following format:\n\n"
        f"Melody: <space-separated list of notes>\n"
        f"Description: <1-2 sentence description of the melody's emotion or story>\n\n"
        f"For example:\n"
        f"Melody: E5 G5 Bb5 E5 D5 Eb5 Bb5 G5 F5 D5 C5 Eb5\n"
        f"Description: This melody represents a sense of quiet contemplation, like a person sitting in stillness, waiting for inspiration to strike."
    )

    

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "shapesinc/notch-bxwh",  # Update with the appropriate model name
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # Make the API request
        response = requests.post(f"{BASE_URL}chat/completions", json=data, headers=headers)

        # Check for successful response
        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data['choices'][0]['message']['content']
            lines = response_text.strip().split('\n', 1)
            melody_line = lines[0]
            description_line = lines[1] if len(lines) > 1 else "No description provided."
            return melody_line, description_line
        else:
            raise Exception(f"Error from Shapes API: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"Error in generating music: {str(e)}")
        return "Error generating music", str(e)


def get_audio(ai_output):
    try:
        melody_match = re.search(r"Melody:\s*(.*)", ai_output)
        description_match = re.search(r"Description:\s*(.*)", ai_output)

        melody_line = melody_match.group(1) if melody_match else ""
        description = description_match.group(1) if description_match else ""

        midi_path = create_midi(melody_line, "melody.mid")
        if not midi_path:
            raise Exception("Failed to create MIDI file")

        output_audio = midi_to_wav(midi_path, "melody.wav")
        if not output_audio:
            raise Exception("Failed to convert MIDI to WAV")

        return output_audio

    except Exception as e:
        print(f"Error in get_audio: {str(e)}")
        raise  # ❗️Let generate_music() handle it



@app.route("/generate-music", methods=["POST"])
def generate_music():
    try:
        data = request.get_json()
        scale = data.get('scale')
        length = data.get('length')

        if not isinstance(length, int):
            try:
                length = int(length)
            except:
                return jsonify({'error': 'Length must be an integer'}), 400

        melody_line, description_line = generate_music_prompt(scale, length)

        output_audio = get_audio(melody_line)

        return send_file(output_audio, as_attachment=True, download_name="melody.wav")

    except Exception as e:
        print(f"Error in generate_music: {e}")
        return jsonify({"error": f"Error generating music: {str(e)}"}), 500



@app.route('/chat', methods=['POST'])
def chat_with_shape():
    try:
        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "shapesinc/notch-bxwh",  # Replace with the correct model name
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(f"{BASE_URL}chat/completions", json=data, headers=headers)

        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            return jsonify({'reply': reply})
        else:
            return jsonify({'error': f"API error: {response.status_code}, {response.text}"}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run()
