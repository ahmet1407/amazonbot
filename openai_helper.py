import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_comment(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ürün analizleri yapan bir uzman gibi davran."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()
