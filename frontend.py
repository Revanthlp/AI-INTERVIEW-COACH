import streamlit as st
import requests

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯"
)

st.title("🎯 AI Interview Coach")

st.write("Welcome to your AI-powered interview preparation assistant!")

st.info("Frontend is working successfully.")

if st.button("Check Backend"):
    response = requests.get("http://127.0.0.1:8000/health")

    if response.status_code == 200:
        st.success("Backend is connected successfully!")
        st.json(response.json())
    else:
        st.error("Backend connection failed.")