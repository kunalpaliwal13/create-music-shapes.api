from flask import Flask, request, jsonify
from openai import OpenAI
from midi import create_midi, midi_to_wav
import shutil
import os

app = Flask(__name__)

shapes_client = OpenAI(
    api_key=os.getenv("API_KEY"),  
    base_url="https://api.shapes.inc/v1/"
)

def generate_music_prompt(scale="C_major", length=16):
    prompt = (
        f"Generate a melody in the {scale} scale with {length} notes. Make the notes have a certain octave, and feel free to use sharps and flats. "
        f"Then write a 1-2 sentence description about what the melody represents."
    ) 
    
    response = shapes_client.chat.completions.create(
        model="shapesinc/notch-bxwh",  
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response

@app.route("/generate-music", methods=["POST"])
def generate_music():
    try:
        data = request.get_json()
        scale = data.get('scale', 'C_major')
        length = data.get('length', 16)

        # Generate music using the LLM
        response = generate_music_prompt(scale, length)
        
        # Extract the music-related text or melody from the response
        response_text = response.choices[0].message.content
        lines = response_text.strip().split('\n', 1)
        melody_line = lines[0]
        description_line = lines[1] if len(lines) > 1 else "No description provided."
        
        output_audio = get_audio(melody_line)
        return send_file(output_audio, as_attachment=True)
        print(jsonify({"generated_music": melody_line, "description": description_line}))

        # return jsonify({"generated_music": generated_music}), 200
    except Exception as e:
        return jsonify({"generated_music": melody_line.strip(), "description": description_line.strip()}), 200


def get_audio(melody_line):
    try:
        melody= melody_line.split('is:')[-1].strip()
        notes = melody.replace(" - ", " ")
        notes = notes.split(" ")
        note_lst = ""
        for i in notes:
            note_lst += (i+ " ")    
        midi_path = create_midi(note_lst, "melody.mid")
        output_audio = midi_to_wav(midi_path, "melody.wav")
        return output_audio
        
@app.route('/chat', methods=['POST'])
def chat_with_shape():
    try:
        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        response = shapes_client.chat.completions.create(
            model="shapesinc/notch-bxwh",  
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message['content']
        return jsonify({'reply': reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
