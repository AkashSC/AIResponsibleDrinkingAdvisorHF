import streamlit as st
import requests
import os

# Hugging Face API Key (set in Render dashboard as env variable)
HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.title("🍷 Responsible Drinking AI Advisor (Open AI Version)")

user_input = st.text_input("Ask your question about drinking responsibly:")

if st.button("Get Advice"):
    if not HF_API_KEY:
        st.error("No Hugging Face API key found. Please set HF_API_KEY in Render environment.")
    else:
        output = query({"inputs": user_input})
        st.write("### AI Advice:")
        st.write(output)
