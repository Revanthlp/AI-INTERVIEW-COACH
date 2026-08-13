import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)


st.title("🎯 AI Interview Coach")

st.write(
    "Practice interview questions, generate AI answers, "
    "evaluate your responses, and get detailed interview scores."
)


# ============================================================
# SESSION STATE
# ============================================================

if "interview_history" not in st.session_state:

    st.session_state.interview_history = []


if "last_evaluation" not in st.session_state:

    st.session_state.last_evaluation = None


# ============================================================
# BACKEND CONNECTION
# ============================================================

st.divider()

st.subheader("🔌 Backend Connection")


if st.button("Check Backend"):

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=10
        )

        if response.status_code == 200:

            st.success(
                "Backend is connected successfully!"
            )

            st.json(
                response.json()
            )

        else:

            st.error(
                f"Backend returned status code: "
                f"{response.status_code}"
            )

    except requests.exceptions.RequestException as error:

        st.error(
            "Could not connect to the FastAPI backend."
        )

        st.code(
            str(error)
        )


# ============================================================
# GENERATE INTERVIEW ANSWER
# ============================================================

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

        st.warning(
            "Please enter an interview question."
        )

    else:

        try:

            with st.spinner(
                "AI is generating an answer..."
            ):

                response = requests.post(
                    f"{API_URL}/answer",
                    json={
                        "question": question
                    },
                    timeout=180
                )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    "Answer generated!"
                )

                st.subheader(
                    "💡 AI Answer"
                )

                st.write(
                    data["answer"]
                )

            else:

                st.error(
                    f"Backend returned status code: "
                    f"{response.status_code}"
                )

        except requests.exceptions.RequestException as error:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.code(
                str(error)
            )


# ============================================================
# EVALUATE CANDIDATE ANSWER
# ============================================================

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
    placeholder=(
        "Type the answer you would give "
        "in an interview..."
    ),
    height=180,
    key="candidate_answer"
)


if st.button("Evaluate My Answer"):

    if not evaluation_question.strip():

        st.warning(
            "Please enter the interview question."
        )

    elif not candidate_answer.strip():

        st.warning(
            "Please enter your answer."
        )

    else:

        try:

            with st.spinner(
                "AI is evaluating your answer..."
            ):

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

                st.success(
                    "Answer evaluated!"
                )

                st.subheader(
                    "📊 AI Feedback"
                )

                st.write(
                    data["evaluation"]
                )

            else:

                st.error(
                    f"Backend returned status code: "
                    f"{response.status_code}"
                )

                st.code(
                    response.text
                )

        except requests.exceptions.RequestException as error:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.code(
                str(error)
            )


# ============================================================
# INTERVIEW SCORE
# ============================================================

st.divider()

st.subheader("⭐ Interview Score")


if st.button("Calculate Score"):

    if not evaluation_question.strip():

        st.warning(
            "Please enter the interview question."
        )

    elif not candidate_answer.strip():

        st.warning(
            "Please enter your answer."
        )

    else:

        try:

            with st.spinner(
                "AI is calculating your score..."
            ):

                score_response = requests.post(
                    f"{API_URL}/score",
                    json={
                        "question": evaluation_question,
                        "answer": candidate_answer
                    },
                    timeout=180
                )

            if score_response.status_code == 200:

                score_data = score_response.json()

                st.success(
                    "Score calculated!"
                )

                st.write(
                    score_data["score"]
                )

            else:

                st.error(
                    f"Backend returned status code: "
                    f"{score_response.status_code}"
                )

                st.code(
                    score_response.text
                )

        except requests.exceptions.RequestException as error:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.code(
                str(error)
            )


# ============================================================
# FULL JSON INTERVIEW EVALUATION
# ============================================================

st.divider()

st.subheader(
    "🎯 AI Interview Performance Report"
)

st.write(
    "Get a structured evaluation with individual scores, "
    "strengths, improvements, and a better answer."
)


if st.button(
    "Generate Performance Report"
):

    if not evaluation_question.strip():

        st.warning(
            "Please enter the interview question."
        )

    elif not candidate_answer.strip():

        st.warning(
            "Please enter your answer."
        )

    else:

        try:

            with st.spinner(
                "AI is analyzing your interview answer..."
            ):

                response = requests.post(
                    f"{API_URL}/json-evaluate",
                    json={
                        "question": evaluation_question,
                        "answer": candidate_answer
                    },
                    timeout=180
                )

            if response.status_code == 200:

                data = response.json()

                # ====================================================
                # SAVE EVALUATION TO INTERVIEW SESSION
                # ====================================================

                session_record = {
                    "question": evaluation_question.strip(),
                    "answer": candidate_answer.strip(),
                    "overall_score": int(
                        data.get("overall_score", 0)
                    ),
                    "correctness": int(
                        data.get("correctness", 0)
                    ),
                    "relevance": int(
                        data.get("relevance", 0)
                    ),
                    "clarity": int(
                        data.get("clarity", 0)
                    ),
                    "completeness": int(
                        data.get("completeness", 0)
                    ),
                    "strengths": data.get(
                        "strengths",
                        []
                    ),
                    "improvements": data.get(
                        "improvements",
                        []
                    ),
                    "better_answer": data.get(
                        "better_answer",
                        ""
                    )
                }


                st.session_state.interview_history.append(
                    session_record
                )


                st.session_state.last_evaluation = (
                    session_record
                )


                st.success(
                    "Performance report generated!"
                )


                # ====================================================
                # CURRENT PERFORMANCE REPORT
                # ====================================================

                st.subheader(
                    "📊 Overall Performance"
                )

                st.metric(
                    "Overall Score",
                    f"{data['overall_score']}/10"
                )


                st.subheader(
                    "📈 Evaluation Breakdown"
                )

                col1, col2, col3, col4 = st.columns(4)


                with col1:

                    st.metric(
                        "Correctness",
                        f"{data['correctness']}/10"
                    )


                with col2:

                    st.metric(
                        "Relevance",
                        f"{data['relevance']}/10"
                    )


                with col3:

                    st.metric(
                        "Clarity",
                        f"{data['clarity']}/10"
                    )


                with col4:

                    st.metric(
                        "Completeness",
                        f"{data['completeness']}/10"
                    )


                st.subheader(
                    "💪 Strengths"
                )

                if data["strengths"]:

                    for strength in data["strengths"]:

                        st.success(
                            f"✓ {strength}"
                        )

                else:

                    st.info(
                        "No specific strengths were returned."
                    )


                st.subheader(
                    "⚠️ Improvements"
                )

                if data["improvements"]:

                    for improvement in data["improvements"]:

                        st.warning(
                            f"• {improvement}"
                        )

                else:

                    st.info(
                        "No specific improvements were returned."
                    )


                st.subheader(
                    "🎯 Better Answer"
                )

                st.info(
                    data["better_answer"]
                )


            else:

                st.error(
                    f"Backend returned status code: "
                    f"{response.status_code}"
                )

                st.code(
                    response.text
                )


        except requests.exceptions.RequestException as error:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.code(
                str(error)
            )


# ============================================================
# INTERVIEW SESSION SUMMARY
# ============================================================

st.divider()

st.subheader(
    "📋 Interview Session Summary"
)


history = st.session_state.interview_history


if not history:

    st.info(
        "Complete at least one performance report "
        "to start your interview session."
    )

else:

    total_questions = len(history)


    average_overall = (
        sum(
            item["overall_score"]
            for item in history
        )
        / total_questions
    )


    average_correctness = (
        sum(
            item["correctness"]
            for item in history
        )
        / total_questions
    )


    average_relevance = (
        sum(
            item["relevance"]
            for item in history
        )
        / total_questions
    )


    average_clarity = (
        sum(
            item["clarity"]
            for item in history
        )
        / total_questions
    )


    average_completeness = (
        sum(
            item["completeness"]
            for item in history
        )
        / total_questions
    )


    # ========================================================
    # FIND STRONGEST AND WEAKEST AREAS
    # ========================================================

    category_scores = {
        "Correctness": average_correctness,
        "Relevance": average_relevance,
        "Clarity": average_clarity,
        "Completeness": average_completeness
    }


    strongest_area = max(
        category_scores,
        key=category_scores.get
    )


    weakest_area = min(
        category_scores,
        key=category_scores.get
    )


    # ========================================================
    # SESSION METRICS
    # ========================================================

    summary_col1, summary_col2, summary_col3 = st.columns(3)


    with summary_col1:

        st.metric(
            "Questions Completed",
            total_questions
        )


    with summary_col2:

        st.metric(
            "Average Score",
            f"{average_overall:.1f}/10"
        )


    with summary_col3:

        st.metric(
            "Strongest Area",
            strongest_area
        )


    st.subheader(
        "📈 Session Performance"
    )


    metric_col1, metric_col2 = st.columns(2)


    with metric_col1:

        st.metric(
            "Average Correctness",
            f"{average_correctness:.1f}/10"
        )

        st.metric(
            "Average Clarity",
            f"{average_clarity:.1f}/10"
        )


    with metric_col2:

        st.metric(
            "Average Relevance",
            f"{average_relevance:.1f}/10"
        )

        st.metric(
            "Average Completeness",
            f"{average_completeness:.1f}/10"
        )


    st.subheader(
        "💡 Interview Coaching Insight"
    )


    if average_overall >= 8:

        st.success(
            f"Great performance! Your current average is "
            f"{average_overall:.1f}/10. Keep practicing "
            f"to make your answers more consistent."
        )

    elif average_overall >= 6:

        st.warning(
            f"Your current average is "
            f"{average_overall:.1f}/10. "
            f"Focus especially on your {weakest_area.lower()} "
            f"to improve your interview performance."
        )

    else:

        st.error(
            f"Your current average is "
            f"{average_overall:.1f}/10. "
            f"Focus on building stronger and more complete "
            f"answers, especially in {weakest_area.lower()}."
        )


    st.info(
        f"Strongest area: {strongest_area} "
        f"({category_scores[strongest_area]:.1f}/10)\n\n"
        f"Area to improve: {weakest_area} "
        f"({category_scores[weakest_area]:.1f}/10)"
    )


    # ========================================================
    # QUESTION-BY-QUESTION HISTORY
    # ========================================================

    st.subheader(
        "📝 Question History"
    )


    for index, item in enumerate(
        history,
        start=1
    ):

        with st.expander(
            f"Question {index}: "
            f"{item['question']}"
        ):

            st.write(
                "**Your Answer:**"
            )

            st.write(
                item["answer"]
            )


            history_col1, history_col2, history_col3 = st.columns(3)


            with history_col1:

                st.metric(
                    "Overall",
                    f"{item['overall_score']}/10"
                )


            with history_col2:

                st.metric(
                    "Correctness",
                    f"{item['correctness']}/10"
                )


            with history_col3:

                st.metric(
                    "Clarity",
                    f"{item['clarity']}/10"
                )


            st.write(
                "**Relevance:** "
                f"{item['relevance']}/10"
            )


            st.write(
                "**Completeness:** "
                f"{item['completeness']}/10"
            )


            if item["strengths"]:

                st.write(
                    "**Strengths:**"
                )

                for strength in item["strengths"]:

                    st.success(
                        f"✓ {strength}"
                    )


            if item["improvements"]:

                st.write(
                    "**Improvements:**"
                )

                for improvement in item["improvements"]:

                    st.warning(
                        f"• {improvement}"
                    )


            st.write(
                "**Better Answer:**"
            )

            st.info(
                item["better_answer"]
            )


    # ========================================================
    # CLEAR SESSION
    # ========================================================

    st.divider()

    if st.button(
        "🗑️ Clear Interview Session"
    ):

        st.session_state.interview_history = []

        st.session_state.last_evaluation = None

        st.success(
            "Interview session cleared."
        )

        st.rerun()


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

st.divider()

st.subheader(
    "📚 Interview Questions"
)


if st.button(
    "Load Questions"
):

    try:

        response = requests.get(
            f"{API_URL}/questions",
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            st.success(
                f"Loaded {data['count']} "
                "interview questions."
            )

            for item in data["questions"]:

                st.markdown(
                    f"**{item['id']}. "
                    f"{item['question']}**"
                )

                st.caption(
                    f"Category: {item['category']} | "
                    f"Difficulty: {item['difficulty']}"
                )

                st.divider()

        else:

            st.error(
                f"Backend returned status code: "
                f"{response.status_code}"
            )

    except requests.exceptions.RequestException as error:

        st.error(
            "Could not connect to the FastAPI backend."
        )

        st.code(
            str(error)
        )
