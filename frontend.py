import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯"
)


st.title("🎯 AI Interview Coach")

st.write(
    "Practice interview questions and prepare for your technical and HR interviews."
)


if st.button("Check Backend"):
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=10
        )

        if response.status_code == 200:
            st.success("Backend is connected successfully!")
            st.json(response.json())
        else:
            st.error(
                f"Backend returned status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as error:
        st.error("Could not connect to the FastAPI backend.")
        st.code(str(error))


st.divider()

st.subheader("📚 Interview Questions")


if st.button("Load Questions"):
    try:
        response = requests.get(
            f"{API_URL}/questions",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            st.success(
                f"Loaded {data['count']} interview questions."
            )

            for question in data["questions"]:
                st.markdown(
                    f"**{question['id']}. {question['question']}**"
                )

                st.caption(
                    f"Category: {question['category']} | "
                    f"Difficulty: {question['difficulty']}"
                )

                st.divider()

        else:
            st.error(
                f"Backend returned status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as error:
        st.error("Could not connect to the FastAPI backend.")
        st.code(str(error))