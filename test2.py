import os
import re
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    for fname in ["api_key.txt", "apikey.txt"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as f:
                raw_key = f.read()
                match = re.search(r'AIza[a-zA-Z0-9_-]+', raw_key)
                if match:
                    api_key = match.group(0)
                    break

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable or api_key.txt required.")

# Connect using the modern SDK
client = genai.Client(api_key=api_key)

print("--- ALL AVAILABLE MODELS ---")
for model in client.models.list():
    print(model.name)
