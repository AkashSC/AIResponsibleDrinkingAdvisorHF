import streamlit as st
import requests
import os

# Hugging Face API Key (set this in Render environment variables)
HF_API_KEY = os.getenv("HF_API_KEY")

# ✅ Free model available on Hugging Face
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return {"error": f"API error {response.status_code}: {response.text}"}
    return response.json()

st.title("🍷 Responsible Drinking AI Advisor (Open AI Version)")

user_input = st.text_input("Enter your drinking info (e.g., 'I had 3 beers' or 'I consumed 30% liquor'): ")

if st.button("Get Advice"):
    if not HF_API_KEY:
        st.error("No Hugging Face API key found. Please set HF_API_KEY in Render environment.")
    else:
        raw_output = query({
            "inputs": f"User consumed: {user_input}. Give responsible drinking advice."
        })

        if "error" in raw_output:
            st.error(raw_output["error"])
        else:
            # Hugging Face returns {"generated_text": "..."} or similar
            advice = raw_output[0].get("generated_text") if isinstance(raw_output, list) else raw_output
            st.write("### AI Advice:")
            st.success(f"{advice}\n\n🚨 Remember: Never drink and drive. Stay hydrated and know your limits.")
