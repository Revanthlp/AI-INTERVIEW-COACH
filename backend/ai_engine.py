import json

from transformers import pipeline


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


print("Loading AI model...")

generator = pipeline(
    "text-generation",
    model=MODEL_NAME
)

print("AI model loaded successfully!")


def _generate(messages, max_new_tokens=150):

    result = generator(
        messages,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        clean_up_tokenization_spaces=False,
    )

    generated_text = result[0]["generated_text"]

    if isinstance(generated_text, list):

        return generated_text[-1]["content"].strip()

    return generated_text.strip()


def generate_answer(question: str) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI Interview Coach. "
                "Give clear, accurate and concise answers "
                "suitable for a fresher technical interview."
            ),
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    return _generate(messages, 150)


def evaluate_answer(
    question: str,
    answer: str
) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional technical interview evaluator. "
                "Evaluate a fresher's answer. "
                "Explain what was done well, what needs improvement, "
                "and give one specific suggestion for a better answer."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Interview Question:\n{question}\n\n"
                f"Candidate Answer:\n{answer}\n\n"
                "Evaluate this answer."
            ),
        },
    ]

    return _generate(messages, 200)


def score_answer(
    question: str,
    answer: str
) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional technical interview evaluator. "
                "Score the candidate's answer from 0 to 10. "
                "Consider correctness, relevance, clarity and completeness. "
                "Return the score first in this format: Score: X/10. "
                "Then briefly explain the reason."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Interview Question:\n{question}\n\n"
                f"Candidate Answer:\n{answer}"
            ),
        },
    ]

    return _generate(messages, 120)


def structured_evaluate_answer(
    question: str,
    answer: str
) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional technical interview evaluator "
                "for fresher candidates.\n\n"

                "Evaluate the candidate answer using these four criteria:\n"
                "1. Correctness\n"
                "2. Relevance\n"
                "3. Clarity\n"
                "4. Completeness\n\n"

                "Give each criterion a score from 0 to 10.\n"
                "Then calculate an overall score from 0 to 10.\n\n"

                "Return the response exactly in this format:\n\n"

                "Overall Score: X/10\n"
                "Correctness: X/10\n"
                "Relevance: X/10\n"
                "Clarity: X/10\n"
                "Completeness: X/10\n\n"

                "Strengths:\n"
                "- point 1\n"
                "- point 2\n\n"

                "Improvements:\n"
                "- point 1\n"
                "- point 2\n\n"

                "Better Answer:\n"
                "A concise improved interview answer."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Interview Question:\n{question}\n\n"
                f"Candidate Answer:\n{answer}"
            ),
        },
    ]

    return _generate(messages, 250)


def json_evaluate_answer(
    question: str,
    answer: str
):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional technical interview evaluator "
                "for fresher candidates.\n\n"

                "Evaluate the candidate's answer fairly.\n\n"

                "Evaluate:\n"
                "1. correctness\n"
                "2. relevance\n"
                "3. clarity\n"
                "4. completeness\n\n"

                "Each score must be an INTEGER from 0 to 10.\n"
                "The overall_score must be an INTEGER from 0 to 10.\n\n"

                "IMPORTANT:\n"

                "- Always provide at least one strength when the "
                "candidate gives correct information.\n"

                "- Always provide at least one improvement unless "
                "the answer is exceptionally complete.\n"

                "- Do not invent mistakes.\n"

                "- Improvements must be useful interview advice.\n"

                "- better_answer must directly answer the question.\n"

                "- better_answer must be a complete standalone answer.\n"

                "- Do NOT return placeholder text such as "
                "'Improved interview answer'.\n"

                "- Do NOT return 'No direct answer provided'.\n"

                "- Do NOT put labels before the better answer.\n\n"

                "Return ONLY valid JSON.\n"
                "Do not use markdown.\n"
                "Do not use ```json.\n"
                "Do not add explanations outside JSON.\n\n"

                "Use this JSON structure:\n"
                "{\n"
                '  "overall_score": 8,\n'
                '  "correctness": 8,\n'
                '  "relevance": 8,\n'
                '  "clarity": 8,\n'
                '  "completeness": 8,\n'
                '  "strengths": ["strength 1"],\n'
                '  "improvements": ["improvement 1"],\n'
                '  "better_answer": "Write the actual improved answer here"\n'
                "}"
            ),
        },
        {
            "role": "user",
            "content": (
                f"Interview Question:\n{question}\n\n"
                f"Candidate Answer:\n{answer}"
            ),
        },
    ]

    raw_response = _generate(
        messages,
        300
    )

    try:

        evaluation = json.loads(
            raw_response
        )

    except json.JSONDecodeError:

        start = raw_response.find("{")
        end = raw_response.rfind("}")

        if start == -1 or end == -1:

            return {
                "overall_score": 0,
                "correctness": 0,
                "relevance": 0,
                "clarity": 0,
                "completeness": 0,
                "strengths": [
                    "The AI response could not be parsed."
                ],
                "improvements": [
                    "Please try the evaluation again."
                ],
                "better_answer": answer.strip()
            }

        try:

            evaluation = json.loads(
                raw_response[start:end + 1]
            )

        except json.JSONDecodeError:

            return {
                "overall_score": 0,
                "correctness": 0,
                "relevance": 0,
                "clarity": 0,
                "completeness": 0,
                "strengths": [
                    "The AI response could not be parsed."
                ],
                "improvements": [
                    "Please try the evaluation again."
                ],
                "better_answer": answer.strip()
            }


    # ========================================================
    # SCORE NORMALIZATION
    # ========================================================

    score_fields = [
        "overall_score",
        "correctness",
        "relevance",
        "clarity",
        "completeness"
    ]

    for field in score_fields:

        value = evaluation.get(
            field,
            0
        )

        try:

            value = int(value)

        except (TypeError, ValueError):

            value = 0

        evaluation[field] = max(
            0,
            min(10, value)
        )


    # ========================================================
    # STRENGTHS
    # ========================================================

    strengths = evaluation.get(
        "strengths",
        []
    )

    if not isinstance(
        strengths,
        list
    ):

        strengths = [
            str(strengths)
        ]

    strengths = [
        str(item).strip()
        for item in strengths
        if str(item).strip()
    ]

    if not strengths and answer.strip():

        strengths.append(
            "The candidate provided a relevant response to the question."
        )


    # ========================================================
    # IMPROVEMENTS
    # ========================================================

    improvements = evaluation.get(
        "improvements",
        []
    )

    if not isinstance(
        improvements,
        list
    ):

        improvements = [
            str(improvements)
        ]

    improvements = [
        str(item).strip()
        for item in improvements
        if str(item).strip()
    ]

    if not improvements:

        improvements.append(
            "Add one or two specific details or examples "
            "to make the answer stronger."
        )


    # ========================================================
    # BETTER ANSWER
    # ========================================================

    better_answer = evaluation.get(
        "better_answer",
        ""
    )

    if not isinstance(
        better_answer,
        str
    ):

        better_answer = str(
            better_answer
        )

    better_answer = better_answer.strip()


    # Remove common labels.

    prefixes = [
        "Improved interview answer:",
        "Better Answer:",
        "Better answer:",
        "Improved Answer:",
        "Improved answer:"
    ]

    for prefix in prefixes:

        if better_answer.startswith(prefix):

            better_answer = (
                better_answer[
                    len(prefix):
                ].strip()
            )


    # Detect placeholder responses.

    invalid_better_answers = [
        "",
        "No direct answer provided.",
        "No direct answer provided",
        "Improved interview answer",
        "Improved Interview Answer",
        "Better Answer",
        "Better answer",
        "Improved Answer",
        "Improved answer",
        "Write the actual improved answer here",
        "Write an improved interview answer here",
        "N/A",
        "None",
        "Not provided"
    ]


    if better_answer in invalid_better_answers:

        better_answer = answer.strip()


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    evaluation["strengths"] = strengths

    evaluation["improvements"] = improvements

    evaluation["better_answer"] = better_answer


    return evaluation