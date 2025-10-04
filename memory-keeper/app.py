import os
import json
from datetime import datetime
import streamlit as st
from gtts import gTTS
from dotenv import load_dotenv
from blog_generator import generate_blog, export_pdf

# ===== Load .env =====
load_dotenv()

# ===== Streamlit Config =====
st.set_page_config(page_title="Memory Keeper for Grandparents", layout="centered")
st.title("👵 Memory Keeper for Grandparents")
st.write("Let’s preserve your memories for future generations 💖")

# ===== Questions =====
QUESTIONS = [
    "What is your favorite childhood memory?",
    "Who was your best friend growing up?",
    "What traditions did your family have?",
    "What was the happiest moment in your life?",
    "What advice would you like to give future generations?"
]

# ===== Data file =====
DATA_FILE = "data/memories.json"
if not os.path.exists("data"):
    os.makedirs("data")

# Load existing answers
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        answers = json.load(f)
else:
    answers = {}

# ===== Chat Interface =====
st.subheader("✍ Share Your Memories")
for i, q in enumerate(QUESTIONS):
    answers[q] = st.text_area(f"Q{i+1}: {q}", value=answers.get(q, ""), height=100)

# ===== Save Answers =====
if st.button("💾 Save My Answers"):
    with open(DATA_FILE, "w") as f:
        json.dump(answers, f, indent=4)
    st.success("✅ Answers saved!")

# ===== Generate Blog =====
if st.button("📝 Generate Memory Blog with AI"):
    blog_html = generate_blog(answers)
    st.components.v1.html(blog_html, height=500, scrolling=True)

    # Download HTML
    st.download_button(
        "⬇ Download Blog (HTML)",
        data=blog_html,
        file_name="memory_blog.html",
        mime="text/html"
    )

    # Generate PDF safely
    pdf_file = export_pdf(blog_html)
    if pdf_file and os.path.exists(pdf_file):
        with open(pdf_file, "rb") as f:
            st.download_button(
                "⬇ Download Blog (PDF)",
                f,
                file_name=os.path.basename(pdf_file),
                mime="application/pdf"
            )
    else:
        st.error("⚠️ PDF generation failed.")

# ===== Show old PDFs =====
st.subheader("📂 Previously Generated PDFs")
pdf_dir = "pdf"
log_file = os.path.join(pdf_dir, "pdf_log.json")
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        logs = json.load(f)
    for entry in reversed(logs):
        file_path = os.path.join(pdf_dir, entry["filename"])
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    f"⬇ {entry['filename']} ({entry['generated_at'][:16]})",
                    f,
                    file_name=entry["filename"],
                    mime="application/pdf"
                )
else:
    st.info("No PDFs generated yet.")

# ===== Text-to-Speech =====
if st.button("🔊 Read My Memories"):
    text = "\n".join([f"{q}: {a}" for q, a in answers.items() if a.strip()])
    if text:
        tts = gTTS(text)
        audio_file = "data/memories.mp3"
        tts.save(audio_file)
        audio_bytes = open(audio_file, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.warning("Please answer some questions first.")
