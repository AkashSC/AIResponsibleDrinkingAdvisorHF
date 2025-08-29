from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

# Hugging Face API key and public model
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL = "bigscience/bloom-560m"

def get_ai_advice(prompt):
    """Call Hugging Face Inference API"""
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers=headers,
        json=payload,
    )

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, list):
            return str(result[0])
        elif "error" in result:
            return f"Error: {result['error']}"
        else:
            return str(result)
    else:
        return f"HTTP Error {response.status_code}: {response.text}"

# HTML template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Responsible Drinking Advisor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
        .container { max-width: 700px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; }
        label { font-weight: bold; }
        input, textarea, select { width: 100%; padding: 10px; margin: 10px 0; border-radius: 8px; border: 1px solid #ccc; }
        button { background: #2ecc71; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; }
        button:hover { background: #27ae60; }
        .response { margin-top: 20px; padding: 15px; background: #ecf0f1; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🍸 Responsible Drinking Advisor</h2>
        <form method="POST" action="/">
            <label for="question">Ask the AI Advisor:</label>
            <textarea name="question" rows="3"></textarea>

            <label for="drinks">Number of drinks:</label>
            <input type="number" name="drinks" min="0" placeholder="e.g., 3">

            <label for="hours">Hours of drinking:</label>
            <input type="number" name="hours" min="1" placeholder="e.g., 2">

            <label for="weight">Weight (kg):</label>
            <input type="number" name="weight" min="30" max="200" placeholder="e.g., 70">

            <label for="gender">Gender:</label>
            <select name="gender">
                <option value="">--Select--</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
            </select>

            <button type="submit">Get Advice</button>
        </form>

        {% if advice %}
        <div class="response">
            <strong>Advisor says:</strong>
            <p>{{ advice }}</p>
        </div>
        {% endif %}

        {% if hydration %}
        <div class="response">
            <strong>Hydration & BAC Estimate:</strong>
            <p>{{ hydration }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    advice = None
    hydration = None

    if request.method == "POST":
        user_question = request.form.get("question", "")
        drinks = request.form.get("drinks")
        hours = request.form.get("hours")
        weight = request.form.get("weight")
        gender = request.form.get("gender")

        # --- AI Advisor using Hugging Face ---
        if user_question:
            prompt = (
                "You are a Responsible Drinking Advisor. "
                "Encourage moderation, hydration, and safe behavior. "
                "Never promote binge drinking or unsafe alcohol use. "
                "Provide tips about responsible drinking, local laws, and health.\n\n"
                f"User Question: {user_question}"
            )
            advice = get_ai_advice(prompt)

        # --- BAC-lite Calculator ---
        if drinks and hours and weight and gender:
            try:
                drinks = int(drinks)
                hours = int(hours)
                weight = float(weight)
                r = 0.73 if gender == "male" else 0.66
                weight_lbs = weight * 2.20462
                bac = (drinks * 14 * 5.14) / (weight_lbs * r) - 0.015 * hours
                bac = max(bac, 0)

                if bac < 0.03:
                    status = "Minimal impairment."
                elif bac < 0.06:
                    status = "Mild impairment. You may feel relaxed but should still be cautious."
                elif bac < 0.08:
                    status = "Legally impaired in many countries. Driving is unsafe."
                else:
                    status = "Dangerous level. Do NOT drive and consider stopping immediately."

                hydration = f"Estimated BAC: {bac:.3f}. {status} Always hydrate with water between drinks."

            except Exception as e:
                hydration = f"Error in calculation: {str(e)}"

    return render_template_string(HTML_PAGE, advice=advice, hydration=hydration)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
