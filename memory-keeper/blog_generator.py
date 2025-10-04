import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
from weasyprint import HTML

load_dotenv()
# Load API key (Gemini)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def polish_story(question, answer, model=None):
    if not answer.strip():
        return ""
    prompt = f"""
    Turn the following memory into a warm, family-friendly story.
    Question: {question}
    Answer: {answer}
    Story:
    """
    try:
        # Gemini integration
        if model is None:
            model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return answer

def generate_blog(answers: dict) -> str:
    """Generate HTML blog with polished AI stories and nice CSS."""
    date_str = datetime.now().strftime("%B %d, %Y")
    blog = f"""
    <html>
    <head>
        <title>Family Memories</title>
        <style>
            body {{ font-family: Georgia, serif; background: #f7f3f0; margin: 40px; }}
            h1 {{ color: #5a3e36; text-align: center; }}
            h3 {{ color: #4b3832; margin-top: 30px; }}
            p {{ font-size: 18px; line-height: 1.6; color: #333; }}
            .date {{ color: gray; font-size: 14px; text-align: center; margin-bottom: 20px; }}
            hr {{ border: 1px solid #d4c6b8; }}
            .container {{ background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0px 0px 15px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <div class="container">
        <h1>💖 Family Memories</h1>
        <p class="date">{date_str}</p>
        <hr>
    """

    for q, a in answers.items():
        if a.strip():
            polished = polish_story(q, a)
            blog += f"<h3>{q}</h3><p>{polished}</p>"

    blog += "</div></body></html>"
    return blog

def export_pdf(html_content: str, filename="memory_blog.pdf"):
    """Convert HTML to PDF using WeasyPrint"""
    HTML(string=html_content).write_pdf(filename)
    return filename
