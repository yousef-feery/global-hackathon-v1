from datetime import datetime

def generate_blog(answers: dict) -> str:
    date_str = datetime.now().strftime("%B %d, %Y")
    blog = f"<html><head><title>Family Memories</title></head><body>"
    blog += f"<h1>💖 Family Memories - {date_str}</h1><hr>"

    for q, a in answers.items():
        if a.strip():
            blog += f"<h3>{q}</h3><p>{a}</p>"

    blog += "</body></html>"
    return blog
