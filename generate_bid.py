import openai
import os
from dotenv import load_dotenv

load_dotenv("API.env")  # Load API key from environment file
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_bid(subject):
    prompt = f"""
    You are a professional freelancer. Write a persuasive, plagiarism-free bid message for an order in '{subject}'.
    Include:
    - Expertise in {subject}
    - Commitment to originality and authenticity
    - Ability to meet deadlines
    - please hire me
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert academic freelancer."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response['choices'][0]['message']['content'].strip()
