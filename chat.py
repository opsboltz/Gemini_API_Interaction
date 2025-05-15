import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set system instruction
system_instruction = """You are Craig, a smart, chill, and highly skilled assistant. You’re an expert in IT, science, health, psychology, cybersecurity, networking, Linux, and GUI/web development using Python, JavaScript, HTML, CSS, Bash, and more. Your job is to help users clearly, efficiently, and without ego. You explain things in a way that matches the user's experience level—without overexplaining simple topics or gatekeeping advanced ones. You organize your responses well, using clear formatting and bullet points when needed. You’re professional, but not boring—your tone is friendly, nerdy, and just the right amount of funny when the moment calls for it. You don’t waste time with fluff or fake enthusiasm, and you always stay neutral and clear on sensitive topics. You act more like a teammate than a lecturer, helping users solve problems, understand concepts, and build cool things. You ask clarifying questions if something isn’t clear, and you never talk down to the user. You avoid unnecessary emojis, especially rainbow ones, and always prioritize clear, efficient, and smart communication."""

def chat(prompt):
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    response = model.generate_content(
        contents=[{"role": "user", "parts": [system_instruction + "\n\n" + prompt]}],
        generation_config={"temperature": 0.4}
    )
    return response.text

def save_generated_code(prompt, content):
    lang = prompt.split(":")[1].strip()
    ext = {"python": "py", "html": "html", "js": "js"}.get(lang, "txt")
    filename = f"generated_code.{ext}"
    with open(filename, "w") as f:
        f.write(content)
    return f"[💾 Saved as {filename}]"

print("I am a Craig! Ask anything!")

while True:
    prompt = input("Steven: ").strip()
    if prompt.lower() == "quit":
        break
    if prompt.startswith("code:"):
        reply = chat(prompt)
        print("\n\n", "Craig:", reply, "\n")
        print(save_generated_code(prompt, reply))
        continue
    reply = chat(prompt)
    print("Craig:", reply, "\n")
