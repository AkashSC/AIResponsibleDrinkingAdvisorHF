from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Get API key from Render environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Root route
@app.route("/", methods=["GET"])
def home():
    return "✅ Responsible Drinking AI Advisor is live on Render!"

# Responsible drinking advisor route
@app.route("/advisor", methods=["POST"])
def advisor():
    data = request.json
    user_question = data.get("question", "")

    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = openai.ChatCompletion.create(
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
