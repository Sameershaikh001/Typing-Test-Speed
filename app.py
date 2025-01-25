from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_sentence')
def get_sentence():
    # Read sentences from the text file
    with open('sentences.txt', 'r') as file:
        sentences = file.readlines()

    # Strip any leading/trailing whitespace and select a random sentence
    sentence = random.choice([s.strip() for s in sentences if s.strip()])
    
    return jsonify({"sentence": sentence})

@app.route('/result', methods=['POST'])
def result():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        typed_text = data.get('typed_text', "")
        original_text = data.get('original_text', "")
        time_taken = data.get('time_taken', 0)

        # Validate input
        if not original_text or not time_taken:
            return jsonify({"error": "Invalid input. Ensure 'original_text' and 'time_taken' are provided"}), 400

        if len(original_text) == 0:
            return jsonify({"error": "Original text cannot be empty"}), 400

        # Calculate stats
        words = len(original_text.split())
        wpm = round((words / time_taken) * 60) if time_taken > 0 else 0
        accuracy = round(sum(1 for a, b in zip(typed_text, original_text) if a == b) / len(original_text) * 100) if len(original_text) > 0 else 0

        return jsonify({"wpm": wpm, "accuracy": accuracy})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
