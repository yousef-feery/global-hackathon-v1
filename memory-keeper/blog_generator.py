import os
import json
from datetime import datetime
from weasyprint import HTML
from dotenv import load_dotenv

load_dotenv()

# Load AI clients
GENEMINI_AVAILABLE = False
OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if API_KEY:
        genai.configure(api_key=API_KEY)
        GENEMINI_AVAILABLE = True
except ImportError:
    GENEMINI_AVAILABLE = False

try:
    import openai
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
        OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

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
    """Generate polished HTML blog with cover page and Table of Contents."""
    date_str = datetime.now().strftime("%B %d, %Y")
    toc = "".join([f"<li>{q}</li>" for q in answers if answers[q].strip()])

    blog = f"""
<html>
<head>
<title>Family Memories</title>
<style>
body {{ font-family: Georgia, serif; background: #f7f3f0; margin: 40px; }}
h1 {{ color: #5a3e36; text-align: center; }}
h2 {{ color: #4b3832; text-align: center; margin-top: 10px; }}
h3 {{ color: #4b3832; margin-top: 30px; }}
p {{ font-size: 18px; line-height: 1.6; color: #333; }}
.date {{ color: gray; font-size: 14px; text-align: center; margin-bottom: 20px; }}
hr {{ border: 1px solid #d4c6b8; }}
.container {{ background: #fff; padding: 30px; border-radius: 10px; 
             box-shadow: 0px 0px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }}
li {{ margin-bottom: 5px; }}
</style>
</head>
<body>
<div class="container">
<h1>💖 Family Memories</h1>
<h2>{date_str}</h2>
<hr>
<h3>Table of Contents</h3>
<ul>{toc}</ul>
<hr>
"""

    for q, a in answers.items():
        if a.strip():
            polished = polish_story(q, a)
            blog += f"<div class='container'><h3>{q}</h3><p>{polished}</p></div>"

    blog += "</body></html>"
    return blog

def export_pdf(html_content: str, directory="pdf") -> str:
    """Export HTML content to PDF in a dedicated folder with timestamp and log."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"memory_blog_{timestamp}.pdf"
    filepath = os.path.join(directory, filename)

    # Generate PDF
    HTML(string=html_content).write_pdf(filepath)

    # Log generated PDFs
    log_file = os.path.join(directory, "pdf_log.json")

    # Safe load JSON
    log = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                log = json.load(f)
        except json.JSONDecodeError:
            log = []

    # Save preview (first 50 chars)
    preview = "".join(html_content.splitlines())[:50]
    log.append({
        "filename": filename,
        "generated_at": datetime.now().isoformat(),
        "preview": preview
    })

    with open(log_file, "w") as f:
        json.dump(log, f, indent=4)

    return filepath  # ✅ must be inside the function
