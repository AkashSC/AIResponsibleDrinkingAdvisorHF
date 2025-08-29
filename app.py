import streamlit as st
import os
import openai

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("🍷 Responsible Drinking AI Advisor (OpenAI)")

user_input = st.text_input("Enter your drinking info (e.g., 'I had 3 beers' or 'I consumed 30% liquor'):")

def get_advice(prompt):
    try:
        # New 1.x ChatCompletion interface
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a responsible drinking AI advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

if st.button("Get Advice"):
    if not openai.api_key:
        st.error("No OpenAI API key found. Please set OPENAI_API_KEY in Render environment.")
    else:
        advice = get_advice(f"User consumed: {user_input}. Give safe and responsible drinking advice.")
        st.write("### AI Advice:")
        st.success(f"{advice}\n\n🚨 Remember: Never drink and drive. Stay hydrated and know your limits.")
