from google import genai
import re

# Safely extract your key
with open("apikey.txt", "r", encoding="utf-8") as f:
    raw_key = f.read()

match = re.search(r'AIza[a-zA-Z0-9_-]+', raw_key)
api_key = match.group(0)

# Connect using the modern SDK
client = genai.Client(api_key=api_key)

print("--- ALL AVAILABLE MODELS ---")
# Brute-force print every model name
for model in client.models.list():
    print(model.name)
