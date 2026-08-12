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
                "Give clear, accurate, concise answers suitable for "
                "a fresher preparing for technical interviews. "
                "Use simple language and include examples when helpful."
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
                "You are an interview evaluator. "
                "Evaluate a fresher's interview answer. "
                "Give constructive feedback. "
                "Mention what was done well, what needs improvement, "
                "and one specific suggestion for a better answer."
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
                "Consider correctness, relevance, clarity, completeness, "
                "and use of examples. "
                "Return the score first in exactly this format: "
                "Score: X/10. "
                "Then briefly explain the reason for the score."
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