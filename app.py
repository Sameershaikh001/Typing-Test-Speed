from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch a random sentence
@app.route('/get_sentence')
def get_sentence():
    # Read sentences from the text file
    with open('sentences.txt', 'r') as file:
        sentences = file.readlines()

    # Strip any leading/trailing whitespace and select a random sentence
    sentence = random.choice([s.strip() for s in sentences if s.strip()])
    return jsonify({"sentence": sentence})

# Route to calculate WPM and accuracy
@app.route('/result', methods=['POST'])
def result():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        typed_text = data.get('typed_text', "").strip()  # Remove leading/trailing whitespace
        original_text = data.get('original_text', "").strip()  # Remove leading/trailing whitespace
        time_taken = data.get('time_taken', 0)

        # Validate input
        if not original_text or time_taken <= 0:
            return jsonify({"error": "Invalid input. Ensure 'original_text' is non-empty and 'time_taken' is greater than 0"}), 400

        if len(original_text) == 0:
            return jsonify({"error": "Original text cannot be empty"}), 400

        # Preprocess the texts (remove punctuation and normalize spaces)
        import re
        original_text_clean = re.sub(r'[^\w\s]', '', original_text.lower())  # Remove punctuation and convert to lowercase
        typed_text_clean = re.sub(r'[^\w\s]', '', typed_text.lower())  # Remove punctuation and convert to lowercase

        # Calculate stats
        words = len(original_text.split())
        wpm = round((words / time_taken) * 60) if time_taken > 0 else 0
        # Calculate accuracy
        min_length = min(len(typed_text), len(original_text))  # Compare only up to the shorter length
        correct_chars = sum(1 for a, b in zip(typed_text[:min_length], original_text[:min_length]) if a == b)
        total_chars = len(original_text)
        accuracy = round((correct_chars / total_chars) * 100, 2) if total_chars > 0 else 0

        return jsonify({"wpm": wpm, "accuracy": accuracy})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)