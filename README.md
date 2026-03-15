# 📄 Gemini Resume Tailor & PDF Generator

An AI-powered automation tool using **Google Gemini 2.5 Flash** to tailor resumes to specific JDs.

## 🚀 Key Features
* **AI-Driven Personalization:** Dynamically pulls from your Knowledge Bank.
* **Surgical Extraction:** Uses Regex to isolate resume content from AI conversational text.
* **Professional Rendering:** Converts Markdown to HTML/CSS for high-fidelity PDF output.

## 🛠️ Setup
1. **Install wkhtmltopdf:** `brew install --cask wkhtmltopdf`
2. **Set API Key:** The app pulls from the `GEMINI_API_KEY` environment variable.
3. **Run:** `python3 app.py` (or your specific filename)
