from transformers import pipeline


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


print("Loading AI model...")

generator = pipeline(
    "text-generation",
    model=MODEL_NAME
)

print("AI model loaded successfully!")


def generate_answer(question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI Interview Coach. "
                "Give clear, accurate, concise answers suitable for "
                "a fresher preparing for technical interviews. "
                "Use simple language and include examples when helpful."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    result = generator(
        messages,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )

    generated_text = result[0]["generated_text"]

    if isinstance(generated_text, list):
        answer = generated_text[-1]["content"]
    else:
        answer = generated_text

    return answer.strip()