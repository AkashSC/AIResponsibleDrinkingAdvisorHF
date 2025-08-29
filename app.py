import streamlit as st
import requests
import os

# Hugging Face API Key (set in Render dashboard as env variable)
HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # ✅ Fixed model

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code != 200:
            return {"error": f"API error {response.status_code}: {response.text}"}
        return response.json()
    except Exception as e:
        return {"error": str(e)}

st.title("🍷 Responsible Drinking AI Advisor (Open AI Version)")

user_input = st.text_input("Enter your drinking info (e.g., 'I had 3 beers' or 'I consumed 30% liquor'): ")

if st.button("Get Advice"):
    if not HF_API_KEY:
        st.error("No Hugging Face API key found. Please set HF_API_KEY in Render environment.")
    else:
        raw_output = query({
            "inputs": f"User consumed: {user_input}. Give safe and responsible drinking advice."
        })

        if "error" in raw_output:
            st.error(raw_output["error"])
        else:
            try:
                text_out = raw_output[0]["generated_text"] if isinstance(raw_output, list) else str(raw_output)
            except Exception:
                text_out = str(raw_output)
            
            st.write("### AI Advice:")
            st.success(f"{text_out}\n\n🚨 Remember: Never drink and drive. Stay hydrated and know your limits.")
