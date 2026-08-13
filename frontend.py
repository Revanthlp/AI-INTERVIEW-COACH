import random

import requests
import streamlit as st


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
    "evaluate your responses, and complete realistic "
    "AI-powered interview sessions."
)


# ============================================================
# SESSION STATE
# ============================================================

if "interview_history" not in st.session_state:
    st.session_state.interview_history = []


if "last_evaluation" not in st.session_state:
    st.session_state.last_evaluation = None


# Interview mode state

if "interview_mode" not in st.session_state:
    st.session_state.interview_mode = False


if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = []


if "interview_current_index" not in st.session_state:
    st.session_state.interview_current_index = 0


if "interview_answers" not in st.session_state:
    st.session_state.interview_answers = []


if "interview_category" not in st.session_state:
    st.session_state.interview_category = "All"


if "interview_question_count" not in st.session_state:
    st.session_state.interview_question_count = 3


if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False


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
# STEP 16 — AI INTERVIEW MODE
# ============================================================

st.divider()

st.subheader(
    "🎤 AI Interview Mode"
)

st.write(
    "Take a realistic interview using randomly selected "
    "questions from your interview question bank."
)


# ============================================================
# START INTERVIEW CONFIGURATION
# ============================================================

if not st.session_state.interview_mode:

    st.markdown(
        "### ⚙️ Interview Setup"
    )

    category_options = [
        "All",
        "HR",
        "Python",
        "Machine Learning",
        "GenAI"
    ]

    selected_category = st.selectbox(
        "Choose interview category:",
        category_options,
        key="interview_category_select"
    )

    question_count = st.selectbox(
        "Number of questions:",
        [2, 3, 5, 8],
        index=1,
        key="interview_count_select"
    )

    if st.button(
        "🚀 Start AI Interview"
    ):

        try:

            with st.spinner(
                "Loading interview questions..."
            ):

                response = requests.get(
                    f"{API_URL}/questions",
                    timeout=10
                )

            if response.status_code != 200:

                st.error(
                    f"Backend returned status code: "
                    f"{response.status_code}"
                )

            else:

                data = response.json()

                all_questions = data.get(
                    "questions",
                    []
                )

                # Filter by category

                if selected_category == "All":

                    filtered_questions = all_questions

                else:

                    filtered_questions = [
                        item
                        for item in all_questions
                        if item.get("category")
                        == selected_category
                    ]


                # Make sure enough questions exist

                if not filtered_questions:

                    st.error(
                        "No questions were found for "
                        "the selected category."
                    )

                else:

                    actual_count = min(
                        question_count,
                        len(filtered_questions)
                    )

                    # Randomly select questions

                    selected_questions = random.sample(
                        filtered_questions,
                        actual_count
                    )

                    # Store interview state

                    st.session_state.interview_questions = (
                        selected_questions
                    )

                    st.session_state.interview_current_index = 0

                    st.session_state.interview_answers = []

                    st.session_state.interview_category = (
                        selected_category
                    )

                    st.session_state.interview_question_count = (
                        actual_count
                    )

                    st.session_state.interview_completed = False

                    st.session_state.interview_mode = True

                    st.rerun()


        except requests.exceptions.RequestException as error:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.code(
                str(error)
            )


# ============================================================
# ACTIVE INTERVIEW
# ============================================================

if st.session_state.interview_mode:

    questions = st.session_state.interview_questions

    current_index = (
        st.session_state.interview_current_index
    )


    # ========================================================
    # INTERVIEW HEADER
    # ========================================================

    st.markdown(
        "### 🎤 Interview In Progress"
    )

    st.caption(
        f"Category: "
        f"{st.session_state.interview_category}"
    )

    st.progress(
        (
            current_index
            / len(questions)
        )
    )

    st.write(
        f"Question {current_index + 1} "
        f"of {len(questions)}"
    )


    # ========================================================
    # CURRENT QUESTION
    # ========================================================

    current_question = questions[
        current_index
    ]


    st.info(
        current_question["question"]
    )


    st.caption(
        f"Category: "
        f"{current_question['category']} | "
        f"Difficulty: "
        f"{current_question['difficulty']}"
    )


    interview_answer = st.text_area(
        "Your answer:",
        placeholder=(
            "Speak or type the answer you would "
            "give to the interviewer..."
        ),
        height=200,
        key=f"interview_answer_{current_index}"
    )


    # ========================================================
    # SUBMIT CURRENT ANSWER
    # ========================================================

    if st.button(
        "📤 Submit Answer",
        key=f"submit_interview_{current_index}"
    ):

        if not interview_answer.strip():

            st.warning(
                "Please enter your answer before submitting."
            )

        else:

            try:

                with st.spinner(
                    "AI is evaluating your answer..."
                ):

                    response = requests.post(
                        f"{API_URL}/json-evaluate",
                        json={
                            "question": current_question["question"],
                            "answer": interview_answer
                        },
                        timeout=180
                    )

                if response.status_code == 200:

                    evaluation = response.json()

                    # Save interview answer

                    interview_record = {
                        "question": current_question[
                            "question"
                        ],
                        "answer": interview_answer.strip(),
                        "category": current_question[
                            "category"
                        ],
                        "difficulty": current_question[
                            "difficulty"
                        ],
                        "overall_score": int(
                            evaluation.get(
                                "overall_score",
                                0
                            )
                        ),
                        "correctness": int(
                            evaluation.get(
                                "correctness",
                                0
                            )
                        ),
                        "relevance": int(
                            evaluation.get(
                                "relevance",
                                0
                            )
                        ),
                        "clarity": int(
                            evaluation.get(
                                "clarity",
                                0
                            )
                        ),
                        "completeness": int(
                            evaluation.get(
                                "completeness",
                                0
                            )
                        ),
                        "strengths": evaluation.get(
                            "strengths",
                            []
                        ),
                        "improvements": evaluation.get(
                            "improvements",
                            []
                        ),
                        "better_answer": evaluation.get(
                            "better_answer",
                            ""
                        )
                    }


                    st.session_state.interview_answers.append(
                        interview_record
                    )


                    # Also add to the main history

                    st.session_state.interview_history.append(
                        interview_record
                    )


                    # Show immediate feedback

                    st.success(
                        "Answer submitted and evaluated!"
                    )


                    st.subheader(
                        "📊 Your Score"
                    )

                    score_col1, score_col2, score_col3, score_col4 = (
                        st.columns(4)
                    )


                    with score_col1:

                        st.metric(
                            "Overall",
                            f"{interview_record['overall_score']}/10"
                        )


                    with score_col2:

                        st.metric(
                            "Correctness",
                            f"{interview_record['correctness']}/10"
                        )


                    with score_col3:

                        st.metric(
                            "Relevance",
                            f"{interview_record['relevance']}/10"
                        )


                    with score_col4:

                        st.metric(
                            "Clarity",
                            f"{interview_record['clarity']}/10"
                        )


                    st.write(
                        "**Completeness:** "
                        f"{interview_record['completeness']}/10"
                    )


                    st.subheader(
                        "💪 Strengths"
                    )

                    for strength in interview_record[
                        "strengths"
                    ]:

                        st.success(
                            f"✓ {strength}"
                        )


                    st.subheader(
                        "⚠️ Improvements"
                    )

                    for improvement in interview_record[
                        "improvements"
                    ]:

                        st.warning(
                            f"• {improvement}"
                        )


                    st.subheader(
                        "🎯 Better Answer"
                    )

                    st.info(
                        interview_record[
                            "better_answer"
                        ]
                    )


                    # ====================================================
                    # NEXT QUESTION / FINISH
                    # ====================================================

                    if (
                        current_index
                        + 1
                        >= len(questions)
                    ):

                        st.session_state.interview_completed = True

                    else:

                        st.session_state.interview_current_index += 1


                    st.rerun()


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
# INTERVIEW COMPLETION
# ============================================================

if (
    st.session_state.interview_mode
    and st.session_state.interview_completed
):

    st.divider()

    st.subheader(
        "🏆 Interview Completed!"
    )

    interview_results = (
        st.session_state.interview_answers
    )


    if interview_results:

        result_count = len(
            interview_results
        )


        average_overall = (
            sum(
                item["overall_score"]
                for item in interview_results
            )
            / result_count
        )


        average_correctness = (
            sum(
                item["correctness"]
                for item in interview_results
            )
            / result_count
        )


        average_relevance = (
            sum(
                item["relevance"]
                for item in interview_results
            )
            / result_count
        )


        average_clarity = (
            sum(
                item["clarity"]
                for item in interview_results
            )
            / result_count
        )


        average_completeness = (
            sum(
                item["completeness"]
                for item in interview_results
            )
            / result_count
        )


        completion_col1, completion_col2, completion_col3 = (
            st.columns(3)
        )


        with completion_col1:

            st.metric(
                "Questions",
                result_count
            )


        with completion_col2:

            st.metric(
                "Interview Score",
                f"{average_overall:.1f}/10"
            )


        with completion_col3:

            if average_overall >= 8:

                performance_label = "Excellent"

            elif average_overall >= 6:

                performance_label = "Good"

            elif average_overall >= 4:

                performance_label = "Needs Practice"

            else:

                performance_label = "Needs Improvement"


            st.metric(
                "Performance",
                performance_label
            )


        st.subheader(
            "📈 Final Interview Breakdown"
        )


        final_col1, final_col2, final_col3, final_col4 = (
            st.columns(4)
        )


        with final_col1:

            st.metric(
                "Correctness",
                f"{average_correctness:.1f}/10"
            )


        with final_col2:

            st.metric(
                "Relevance",
                f"{average_relevance:.1f}/10"
            )


        with final_col3:

            st.metric(
                "Clarity",
                f"{average_clarity:.1f}/10"
            )


        with final_col4:

            st.metric(
                "Completeness",
                f"{average_completeness:.1f}/10"
            )


        # ====================================================
        # STRONGEST / WEAKEST AREA
        # ====================================================

        final_category_scores = {
            "Correctness": average_correctness,
            "Relevance": average_relevance,
            "Clarity": average_clarity,
            "Completeness": average_completeness
        }


        strongest_area = max(
            final_category_scores,
            key=final_category_scores.get
        )


        weakest_area = min(
            final_category_scores,
            key=final_category_scores.get
        )


        st.subheader(
            "💡 AI Coaching Summary"
        )


        st.success(
            f"Your strongest area is "
            f"**{strongest_area}** with an average of "
            f"{final_category_scores[strongest_area]:.1f}/10."
        )


        st.warning(
            f"Your main area to improve is "
            f"**{weakest_area}** with an average of "
            f"{final_category_scores[weakest_area]:.1f}/10."
        )


        if average_overall >= 8:

            st.info(
                "You are performing strongly. Focus on "
                "consistency, concise explanations, and "
                "adding relevant examples."
            )

        elif average_overall >= 6:

            st.info(
                "Your foundation is good. Practice giving "
                "more structured answers and strengthen "
                "your weaker evaluation areas."
            )

        else:

            st.info(
                "Keep practicing the fundamentals. "
                "Focus on answering the exact question, "
                "explaining concepts clearly, and adding "
                "simple examples."
            )


        # ====================================================
        # INTERVIEW RESULTS
        # ====================================================

        st.subheader(
            "📝 Interview Results"
        )


        for index, result in enumerate(
            interview_results,
            start=1
        ):

            with st.expander(
                f"Question {index}: "
                f"{result['question']}"
            ):

                st.write(
                    "**Your Answer:**"
                )

                st.write(
                    result["answer"]
                )


                result_col1, result_col2, result_col3 = (
                    st.columns(3)
                )


                with result_col1:

                    st.metric(
                        "Overall",
                        f"{result['overall_score']}/10"
                    )


                with result_col2:

                    st.metric(
                        "Correctness",
                        f"{result['correctness']}/10"
                    )


                with result_col3:

                    st.metric(
                        "Clarity",
                        f"{result['clarity']}/10"
                    )


                st.write(
                    "**Relevance:** "
                    f"{result['relevance']}/10"
                )


                st.write(
                    "**Completeness:** "
                    f"{result['completeness']}/10"
                )


                if result["strengths"]:

                    st.write(
                        "**Strengths:**"
                    )

                    for strength in result["strengths"]:

                        st.success(
                            f"✓ {strength}"
                        )


                if result["improvements"]:

                    st.write(
                        "**Improvements:**"
                    )

                    for improvement in result["improvements"]:

                        st.warning(
                            f"• {improvement}"
                        )


                st.write(
                    "**Better Answer:**"
                )

                st.info(
                    result["better_answer"]
                )


    # ========================================================
    # RESTART INTERVIEW
    # ========================================================

    if st.button(
        "🔄 Start New Interview"
    ):

        st.session_state.interview_mode = False

        st.session_state.interview_questions = []

        st.session_state.interview_current_index = 0

        st.session_state.interview_answers = []

        st.session_state.interview_completed = False

        st.rerun()


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


    summary_col1, summary_col2, summary_col3 = (
        st.columns(3)
    )


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
            f"Focus especially on your "
            f"{weakest_area.lower()} "
            f"to improve your interview performance."
        )

    else:

        st.error(
            f"Your current average is "
            f"{average_overall:.1f}/10. "
            f"Focus on building stronger and more complete "
            f"answers, especially in "
            f"{weakest_area.lower()}."
        )


    st.info(
        f"Strongest area: {strongest_area} "
        f"({category_scores[strongest_area]:.1f}/10)\n\n"
        f"Area to improve: {weakest_area} "
        f"({category_scores[weakest_area]:.1f}/10)"
    )


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


            history_col1, history_col2, history_col3 = (
                st.columns(3)
            )


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


    st.divider()


    if st.button(
        "🗑️ Clear Interview Session"
    ):

        st.session_state.interview_history = []

        st.session_state.last_evaluation = None

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