# 📄 Gemini Resume Slicer & PDF Generator

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini%202.5%20Flash-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev)
[![wkhtmltopdf](https://img.shields.io/badge/PDF-wkhtmltopdf%20%7C%20pdfkit-red?style=for-the-badge)](https://wkhtmltopdf.org)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)](#)

An AI-powered desktop automation workstation utilizing **Google Gemini 2.5 Flash** to analyze complex enterprise job descriptions, match requirements against an extensive multi-role Knowledge Bank, and synthesize tailored, high-impact resumes directly into beautifully styled, print-ready PDF documents.

---

## 🏗️ Architecture & Pipeline

```
  [ Raw Job Description ]
             │
             ▼
  +──────────────────────────────────────────────────────────────+
  |              CustomTkinter Desktop Application               |
  |                        (`app.py`)                            |
  +──────────────────────────────┬───────────────────────────────+
                                 │
     +---------------------------+---------------------------+
     |                                                       |
     v                                                       v
[ Personafile.txt ]                                 [ KnowledgeBank.txt ]
(Executive Profile, Formatting Constraints)         (Project Stories, Scope, Metrics)
     |                                                       |
     +---------------------------+---------------------------+
                                 │
                                 v
  +──────────────────────────────────────────────────────────────+
  |            Google Gemini 2.5 Flash Inference API             |
  |        - Tailors bullet points to specific JD keywords       |
  |        - Slices highest-relevance achievements & metrics     |
  +──────────────────────────────┬───────────────────────────────+
                                 │
                                 v
  +──────────────────────────────────────────────────────────────+
  |                   Regex Anchor Extraction                    |
  |            Isolates structured Markdown payload              |
  +──────────────────────────────┬───────────────────────────────+
                                 │
                                 v
  +──────────────────────────────────────────────────────────────+
  |                HTML5 & CSS Typographic Styling               |
  |                  (`style.css` + `markdown2`)                 |
  +──────────────────────────────┬───────────────────────────────+
                                 │
                                 v
  +──────────────────────────────────────────────────────────────+
  |               `pdfkit` / `wkhtmltopdf` Engine                |
  |            Compiles pixel-perfect, ATS-ready PDF             |
  +──────────────────────────────────────────────────────────────+
```

---

## 🚀 Key Features

* **AI-Driven Personalization:** Dynamically pulls from a structured Knowledge Bank and candidate profile to tailor bullets, metrics, and executive summaries to target job postings.
* **Intelligent Anchor Extraction:** Surgically isolates structured resume content from conversational AI outputs using regex markers.
* **Modern PDF Generation:** Converts Markdown into high-fidelity, print-ready PDFs using HTML5, modern CSS typography (`style.css`), and `wkhtmltopdf`.
* **Cross-Platform Desktop GUI:** Clean, responsive desktop interface built with `customtkinter`.
* **Zero Cloud Lock-in:** Runs entirely on local desktop compute with direct, secure API calls to Gemini.

---

## 🛠️ Requirements & Prerequisites

* **Python 3.10+**
* **wkhtmltopdf**: Required for rendering HTML/CSS to PDF.
  * macOS (Homebrew): `brew install --cask wkhtmltopdf`
  * Linux: `sudo apt-get install wkhtmltopdf`
  * Windows: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html) and add to system PATH.

---

## 📦 Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone git@github.com:Jspaun-00/ResumeBuilder.git
   cd ResumeBuilder
   ```

2. **Install Dependencies:**
   ```bash
   pip install customtkinter markdown2 pdfkit requests python-docx google-genai
   ```

3. **Set Your Gemini API Key:**
   * **Option A (Recommended):** Set the environment variable:
     ```bash
     export GEMINI_API_KEY="your-gemini-api-key-here"
     ```
   * **Option B:** Create a local `api_key.txt` file in the project root containing your key (this file is ignored by `.gitignore`).

4. **Prepare Your Profile & Knowledge Bank:**
   * Copy `Personafile.example.txt` to `Personafile.txt` and customize with your contact information, target structure, and instructions.
   * Copy `KnowledgeBank.example.txt` to `KnowledgeBank.txt` and add your past project stories, achievements, and impact metrics.
   * Place your base `Resume.docx` in the root folder.

---

## 💻 Usage

Run the desktop application:
```bash
python3 app.py
```

1. Paste any Job Description into the input area.
2. Click **Generate Tailored Resume**.
3. The application will synthesize your tailored resume, compile it with CSS typography, and produce `Tailored_Resume.pdf`.

---

## 🔒 Security & Privacy

* **Strictly Anonymized:** Template files (`Personafile.example.txt`, `KnowledgeBank.example.txt`) provide clean structures for public repositories.
* **Local Data Sovereignty:** Personal background data stays solely on the user's machine.
