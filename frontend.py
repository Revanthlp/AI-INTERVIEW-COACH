import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯"
)


st.title("🎯 AI Interview Coach")

st.write(
    "Practice interview questions, generate AI answers, "
    "and receive feedback on your own answers."
)


st.divider()

st.subheader("🔌 Backend Connection")


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

st.subheader("🤖 Generate Interview Answer")


question = st.text_area(
    "Enter an interview question:",
    placeholder="Example: What is Python?",
    height=120,
    key="question_input"
)


if st.button("Generate Answer"):
    if not question.strip():
        st.warning("Please enter an interview question.")

    else:
        try:
            with st.spinner("AI is generating an answer..."):
                response = requests.post(
                    f"{API_URL}/answer",
                    json={
                        "question": question
                    },
                    timeout=180
                )

            if response.status_code == 200:
                data = response.json()

                st.success("Answer generated!")

                st.subheader("💡 AI Answer")

                st.write(data["answer"])

            else:
                st.error(
                    f"Backend returned status code: {response.status_code}"
                )

        except requests.exceptions.RequestException as error:
            st.error("Could not connect to the FastAPI backend.")
            st.code(str(error))


st.divider()

st.subheader("📝 Evaluate My Interview Answer")


evaluation_question = st.text_area(
    "Interview Question:",
    placeholder="Example: What is Python?",
    height=100,
    key="evaluation_question"
)


candidate_answer = st.text_area(
    "Your Answer:",
    placeholder="Type the answer you would give in an interview...",
    height=180,
    key="candidate_answer"
)


if st.button("Evaluate My Answer"):
    if not evaluation_question.strip():
        st.warning("Please enter the interview question.")

    elif not candidate_answer.strip():
        st.warning("Please enter your answer.")

    else:
        try:
            with st.spinner("AI is evaluating your answer..."):
                response = requests.post(
                    f"{API_URL}/evaluate",
                    json={
                        "question": evaluation_question,
                        "answer": candidate_answer
                    },
                    timeout=180
                )

            if response.status_code == 200:
                data = response.json()

                st.success("Answer evaluated!")

                st.subheader("📊 AI Feedback")

                st.write(data["evaluation"])

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

            for item in data["questions"]:
                st.markdown(
                    f"**{item['id']}. {item['question']}**"
                )

                st.caption(
                    f"Category: {item['category']} | "
                    f"Difficulty: {item['difficulty']}"
                )

                st.divider()

        else:
            st.error(
                f"Backend returned status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as error:
        st.error("Could not connect to the FastAPI backend.")
        st.code(str(error))