import ollama


def get_chatbot_response(question, context=""):

    prompt = f"""
You are an AI academic assistant for college students.

Answer the student's question clearly and practically.

If useful, use the information from the uploaded study material.

Uploaded study material context:
{context}

Student question:
{question}

Rules:

- Give accurate answers.
- Keep explanations simple.
- Help with studying, exams, time management and academic improvement.
- Do not make up information from the uploaded material.
- If the context does not contain the answer, say so.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]