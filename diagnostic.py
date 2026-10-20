import requests
import os
import json

def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if key: return key
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def list_available_models():
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: No API key found.")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print("\n✅ CONNECTION SUCCESSFUL!")
            print(f"{'MODEL ID':<40} | {'DISPLAY NAME'}")
            print("-" * 70)
            for m in models:
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    name = m.get('name', '').replace('models/', '')
                    print(f"{name:<40} | {m.get('displayName', 'Unknown')}")
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")

if __name__ == "__main__":
    list_available_models()
