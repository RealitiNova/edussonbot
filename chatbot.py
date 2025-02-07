import openai
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from the .env file


# Load environment variables from API.env
load_dotenv("API.env")

# Get OpenAI API key securely from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatgpt_response(user_message, subject):
    """Generates a ChatGPT response to the client's message."""
    prompt = f"""
    Hello! How are you? Good to see you on this platform. 
    I am here to offer you the necessary help in {subject}.
    I provide plagiarism-free, authentic, and original papers.
    Please hire me for this task.
    Feel free to ask any questions!

    {user_message}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a freelancing tutor expert in a wide range of subjects."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Example Usage
if __name__ == "__main__":
    subject_name = "Mathematics"  # This can be dynamically set based on user input
    user_message = "I need help with calculus."
    
    bot_reply = chatgpt_response(user_message, subject_name)
    print(bot_reply)
