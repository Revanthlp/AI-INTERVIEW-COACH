from transformers import pipeline


print("Loading AI model...")

generator = pipeline(
    "text-generation",
    model="distilgpt2"
)

print("AI model loaded successfully!")


def generate_answer(question: str) -> str:
    prompt = f"Question: {question}\nAnswer:"

    result = generator(
        prompt,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.7,
        pad_token_id=generator.tokenizer.eos_token_id,
        clean_up_tokenization_spaces=False
    )

    generated_text = result[0]["generated_text"]

    if "Answer:" in generated_text:
        answer = generated_text.split("Answer:", 1)[1].strip()
    else:
        answer = generated_text.strip()

    return answer