from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

# Init new OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/advisor", methods=["POST"])
def advisor():
    data = request.get_json(silent=True) or {}
    user_question = data.get("question", "")

    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 
                 "You are a Responsible Drinking Advisor. "
                 "Encourage moderation, hydration, and safe behavior. "
                 "Never promote binge drinking or unsafe alcohol use. "
                 "Provide tips about responsible drinking, local laws, and health."},
                {"role": "user", "content": user_question}
            ]
        )
        return jsonify({"advice": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
