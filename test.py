import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key and os.path.exists("api_key.txt"):
    with open("api_key.txt", "r", encoding="utf-8") as f:
        api_key = f.read().strip()

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable or api_key.txt required.")

genai.configure(api_key=api_key)

print("--- AVAILABLE MODELS ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

