import customtkinter as ctk
from google import genai
import markdown2
import pdfkit
import os
import docx
import re
import threading
import time
import sys

# --- 1. INTEGRATED API KEY & PATHS ---
INTEGRATED_API_KEY = "AIzaSyBO4wFMUzjWavK_K8mzwVlHQwnpp46uDNw"

def get_base_path():
    """Finds the folder where the app icon is sitting, specifically for macOS .app bundles."""
    if getattr(sys, 'frozen', False):
        bundle_dir = os.path.dirname(sys.executable)
        if "Contents/MacOS" in bundle_dir:
            return os.path.abspath(os.path.join(bundle_dir, "../../.."))
        return bundle_dir
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_path()

# Define File Paths
MODEL_NAME = "gemini-2.5-flash"
PERSONA_FILE = os.path.join(BASE_DIR, "Personafile.txt")
KNOWLEDGE_BANK_FILE = os.path.join(BASE_DIR, "KnowledgeBank.txt")
RESUME_FILE = os.path.join(BASE_DIR, "Resume.docx")
CSS_FILE = os.path.join(BASE_DIR, "style.css")
OUTPUT_PDF = os.path.join(BASE_DIR, "Tailored_Resume.pdf")

PATH_TO_WKHTMLTOPDF = '/usr/local/bin/wkhtmltopdf'

# --- 2. LOGIC FUNCTIONS ---

def read_text_file(filepath):
    """Reads external text files reliably."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()
    return ""

def read_docx_file(filepath):
    """Reads the baseline resume docx."""
    if os.path.exists(filepath):
        try:
            doc = docx.Document(filepath)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            print(f"Error reading docx: {e}")
    return ""

def generate_resume_logic(jd, on_complete):
    """Core process: AI Generation -> Surgical Extraction -> Injected CSS PDF."""
    try:
        client = genai.Client(api_key=INTEGRATED_API_KEY)
        
        persona_text = read_text_file(PERSONA_FILE)
        kb_text = read_text_file(KNOWLEDGE_BANK_FILE)
        resume_text = read_docx_file(RESUME_FILE)

        if not persona_text:
            raise Exception(f"Persona file not found at: {PERSONA_FILE}")

        prompt = f"{persona_text}\n\nSOURCES:\nKB: {kb_text}\nRES: {resume_text}\n\nTARGET JD:\n{jd}"

        # --- RETRY LOOP FOR RATE LIMITS ---
        response = None
        for attempt in range(4):
            try:
                response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                if response.text: break
            except Exception as api_err:
                err_msg = str(api_err).lower()
                if ("503" in err_msg or "429" in err_msg or "exhausted" in err_msg) and attempt < 3:
                    wait_time = (2 ** attempt) * 5 
                    time.sleep(wait_time)
                    continue
                raise api_err

        raw_text = response.text
        
        # --- EXTRACTION LOGIC ---
        name_match = re.search(r'(#+ |\*\*?)JEREMY SPAUNHURST', raw_text, re.IGNORECASE)
        end_marker_match = re.search(re.escape("PHASE 7"), raw_text, re.IGNORECASE)

        if name_match:
            start_idx = name_match.start()
            end_idx = end_marker_match.start() if end_marker_match else None
            resume_markdown = raw_text[start_idx:end_idx].strip() if end_idx else raw_text[start_idx:].strip()
        else:
            resume_markdown = raw_text.strip()

        # CLEANUP: Ensure Markdown headers and bullets are clean for the converter
        resume_markdown = re.sub(r'PHASE 6:.*', '', resume_markdown, flags=re.IGNORECASE)
        resume_markdown = resume_markdown.replace('[', '').replace(']', '')
        resume_markdown = re.sub(r'^```markdown|```$', '', resume_markdown, flags=re.IGNORECASE).strip()
        resume_markdown = resume_markdown.strip().rstrip('#*').strip()
        resume_markdown = re.sub(r'\n\s*(\*|-)', r'\n\n\1', resume_markdown)

        # HTML CONVERSION WITH DIRECT CSS INJECTION
        html_content = markdown2.markdown(resume_markdown)
        css_content = read_text_file(CSS_FILE)
        
        # We wrap the HTML and CSS into one single string so pdfkit doesn't have to look for files
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
            {css_content}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        options = {
            'page-size': 'Letter',
            'margin-top': '0.4in',
            'margin-right': '0.4in',
            'margin-bottom': '0.4in',
            'margin-left': '0.4in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)
        pdfkit.from_string(full_html, OUTPUT_PDF, options=options, configuration=config)

        app.after(0, lambda: on_complete(f"Success! Saved to {OUTPUT_PDF}", "green"))

    except Exception as e:
        err_str = str(e)
        app.after(0, lambda: on_complete(f"Error: {err_str}", "red"))

def start_generation_thread():
    jd = textbox.get("1.0", "end-1c")
    if not jd.strip():
        status_label.configure(text="Paste JD first!", text_color="red")
        return

    status_label.configure(text="AI is strategizing...", text_color="yellow")
    generate_button.configure(state="disabled")
    
    threading.Thread(target=generate_resume_logic, args=(jd, _update_ui_after_generation)).start()

def _update_ui_after_generation(msg, color):
    status_label.configure(text=msg, text_color=color)
    generate_button.configure(state="normal")

# --- 3. UI SETUP ---
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.geometry("500x550")
    app.title("Gemini Resume Generator")

    ctk.CTkLabel(app, text="Paste Job Description:", font=("Arial", 14, "bold")).pack(pady=(20, 10))
    textbox = ctk.CTkTextbox(app, width=450, height=350)
    textbox.pack(pady=10)

    generate_button = ctk.CTkButton(app, text="GENERATE PDF", command=start_generation_thread, fg_color="#5B84B1")
    generate_button.pack(pady=10)

    status_label = ctk.CTkLabel(app, text="Ready", text_color="gray")
    status_label.pack(pady=10)

    app.mainloop()