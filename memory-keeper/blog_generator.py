import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# pick a model (like gemini-1.5-flash or gemini-2.5)
model = genai.GenerativeModel("gemini-2.5-flash")

# make a request
def polish_story(question, answer):
    if not answer.strip():
        return ""

    prompt = f"""
    Turn the following memory into a warm, family-friendly story.
    Question: {question}
    Answer: {answer}
    Story:
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return answer  # fallback

def generate_blog(answers: dict) -> str:
    date_str = datetime.now().strftime("%B %d, %Y")
    blog = f"""
    <html>
    <head>
        <title>Family Memories</title>
        <style>
            body {{ font-family: Georgia, serif; margin: 40px; background: #fafafa; }}
            h1 {{ color: #444; }}
            h3 {{ color: #333; margin-top: 20px; }}
            p {{ font-size: 18px; line-height: 1.6; }}
            .date {{ color: gray; font-size: 14px; }}
        </style>
    </head>
    <body>
        <h1>💖 Family Memories</h1>
        <p class="date">{date_str}</p>
        <hr>
    """

    for q, a in answers.items():
        if a.strip():
            polished = polish_story(q, a)
            blog += f"<h3>{q}</h3><p>{polished}</p>"

    blog += "</body></html>"
    return blog
