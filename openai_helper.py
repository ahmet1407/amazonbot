import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_comment(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ürün analizleri yapan bir uzman asistan gibi yanıt ver."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()
