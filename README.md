# 📄 Gemini Resume Slicer & PDF Generator

An AI-powered desktop automation tool using **Google Gemini 2.5 Flash** to analyze job descriptions and synthesize tailored, high-impact resumes directly into beautifully styled PDF documents.

---

## 🚀 Key Features

* **AI-Driven Personalization:** Dynamically pulls from a structured Knowledge Bank and candidate profile to tailor bullets, metrics, and executive summaries to target job postings.
* **Intelligent Anchor Extraction:** Surgically isolates structured resume content from conversational AI outputs using regex markers.
* **Modern PDF Generation:** Converts Markdown into high-fidelity, print-ready PDFs using HTML5, modern CSS typography, and `wkhtmltopdf`.
* **Desktop GUI:** Simple and intuitive desktop interface built with `customtkinter`.

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

1. Paste any Job Description into the text area.
2. Click **GENERATE TAILORED PDF**.
3. Your tailored resume will be compiled and exported directly to `~/Desktop/Tailored_Resume.pdf`.

---

## 📁 Repository Structure

```
.
├── app.py                     # Main CustomTkinter desktop application
├── style.css                  # Modern resume print stylesheet
├── Personafile.example.txt    # Persona and prompt structure template
├── KnowledgeBank.example.txt  # STAR interview and achievement story template
├── diagnostic.py              # API connection and model availability test
├── fast_test.py               # Fast local PDF rendering benchmark
├── test.py                    # Gemini SDK connection test
├── .gitignore                 # Excludes credentials, build dirs, and personal files
└── README.md                  # Documentation
```

---

## 🔒 Security & Privacy

This repository does not store personal contact information or active API credentials. Candidate stories, personal resumes (`*.docx`), generated PDFs (`*.pdf`), and local API key files are excluded via `.gitignore`.
