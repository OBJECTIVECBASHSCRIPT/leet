from flask import Flask, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate-pattern', methods=['GET'])
def generate_pattern():
    prompt = (
        "Generate a numeric pattern of 6 numbers. The pattern should follow a logic "
        "(like Fibonacci, arithmetic, geometric, or other interesting rules). "
        "Replace one number with a '?'. Only output a raw JSON like this:\n"
        '{"pattern": [1, 1, 2, 3, "?", 8], "logic": "Fibonacci"}'
    )

    try:
        response = OpenAI.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )

        text = response['choices'][0]['message']['content'].strip()

        # Try to evaluate safely to Python dict
        pattern_data = eval(text)  # Note: in production, use `json.loads()` with validation!
        return jsonify(pattern_data)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Pattern generation failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
