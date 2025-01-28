import os
import openai
from flask import Flask, request, jsonify, render_template
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI client with the API key
openai_client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Get API key from environment
)

# Check if the API key is loaded
if not openai_client.api_key:
    app.logger.error("OPENAI_API_KEY environment variable not set.")
    raise ValueError("OPENAI_API_KEY environment variable not set.")
else:
    app.logger.info("OpenAI API key loaded successfully.")

@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html is in the 'templates' folder

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    app.logger.info(f"Received user message: {user_message}")

    if not user_message:
        app.logger.warning("No message provided in request.")
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Accessing the message content using dot notation
        bot_message = response.choices[0].message.content.strip()
        app.logger.info(f"Bot response: {bot_message}")
        return jsonify({"response": bot_message})

    except Exception as e:
        app.logger.error(f"Error during OpenAI API call: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
