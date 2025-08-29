from flask import Flask, request, jsonify, render_template_string
import openai
import os

app = Flask(__name__)

# Get API key from Render environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple HTML template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Responsible Drinking Advisor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; }
        input, textarea { width: 100%; padding: 10px; margin: 10px 0; border-radius: 8px; border: 1px solid #ccc; }
        button { background: #2ecc71; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; }
        button:hover { background: #27ae60; }
        .response { margin-top: 20px; padding: 15px; background: #ecf0f1; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🍸 Responsible Drinking Advisor</h2>
        <form method="POST" action="/advisor">
            <label for="question">Ask me anything about drinking responsibly:</label>
            <textarea name="question" rows="3" required></textarea>
            <button type="submit">Get Advice</button>
        </form>
        {% if advice %}
        <div class="response">
            <strong>Advisor says:</strong>
            <p>{{ advice }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    advice = None
    if request.method == "POST":
        user_question = request.form.get("question", "")
        if user_question:
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
                advice = response.choices[0].message.content
            except Exception as e:
                advice = f"Error: {str(e)}"

    return render_template_string(HTML_PAGE, advice=advice)


@app.route("/advisor", methods=["POST"])
def advisor():
    """API endpoint for programmatic access"""
    data = request.json or {}
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
