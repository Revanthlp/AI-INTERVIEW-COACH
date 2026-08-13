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


def evaluate_answer(question: str, answer: str) -> str:

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


def score_answer(question: str, answer: str) -> str:

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


def structured_evaluate_answer(question: str, answer: str) -> str:

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


def json_evaluate_answer(question: str, answer: str):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional technical interview evaluator.\n\n"

                "Evaluate the candidate's answer using these criteria:\n"
                "- correctness\n"
                "- relevance\n"
                "- clarity\n"
                "- completeness\n\n"

                "Each score must be an INTEGER from 0 to 10.\n"
                "The overall_score must also be an INTEGER from 0 to 10.\n\n"

                "Return ONLY valid JSON.\n"
                "Do not use markdown.\n"
                "Do not use ```json.\n"
                "Do not add explanations outside the JSON.\n\n"

                "Use exactly this structure:\n"
                "{\n"
                '  "overall_score": 8,\n'
                '  "correctness": 8,\n'
                '  "relevance": 8,\n'
                '  "clarity": 8,\n'
                '  "completeness": 8,\n'
                '  "strengths": ["strength 1", "strength 2"],\n'
                '  "improvements": ["improvement 1", "improvement 2"],\n'
                '  "better_answer": "Improved interview answer"\n'
                "}\n\n"

                "Make sure the JSON is valid and contains all fields."
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

    raw_response = _generate(messages, 300)

    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:

        start = raw_response.find("{")
        end = raw_response.rfind("}")

        if start != -1 and end != -1:

            json_text = raw_response[
                start:end + 1
            ]

            try:
                return json.loads(json_text)

            except json.JSONDecodeError:
                pass

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
            "better_answer": ""
        }