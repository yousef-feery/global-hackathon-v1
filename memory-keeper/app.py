import streamlit as st
import json
import os
from datetime import datetime
from blog_generator import generate_blog
from gtts import gTTS

# ===== CONFIG =====
DATA_FILE = "data/memories.json"
QUESTIONS = [
    "What is your favorite childhood memory?",
    "Who was your best friend growing up?",
    "What traditions did your family have?",
    "What was the happiest moment in your life?",
    "What advice would you like to give future generations?"
]

st.set_page_config(page_title="Memory Keeper for Grandparents", layout="centered")
st.title("👵 Memory Keeper for Grandparents")
st.write("Let’s preserve your memories for future generations 💖")

# ===== LOAD/INIT ANSWERS =====
if not os.path.exists("data"):
    os.makedirs("data")

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        answers = json.load(f)
else:
    answers = {}

# ===== CHAT INTERFACE =====
st.subheader("✍️ Share Your Memories")
for i, q in enumerate(QUESTIONS):
    answer = st.text_area(f"Q{i+1}: {q}", value=answers.get(q, ""), height=100)
    answers[q] = answer

# ===== SAVE ANSWERS =====
if st.button("💾 Save My Answers"):
    with open(DATA_FILE, "w") as f:
        json.dump(answers, f, indent=4)
    st.success("✅ Answers saved!")

# ===== GENERATE BLOG =====
if st.button("📝 Generate Memory Blog with AI"):
    blog_html = generate_blog(answers)
    blog_file = f"data/memory_blog_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    with open(blog_file, "w") as f:
        f.write(blog_html)

    st.download_button("⬇️ Download Blog (HTML)", data=blog_html, file_name="memory_blog.html", mime="text/html")
    st.components.v1.html(blog_html, height=500, scrolling=True)
    st.success("✅ AI-enhanced blog generated!")

# ===== TEXT TO SPEECH =====
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
