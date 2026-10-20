import customtkinter as ctk
import markdown2
import pdfkit
import os
import docx
import re
import threading
import sys
import requests
import time
import traceback

# --- 1. BULLETPROOF PATH LOGIC ---

def get_resource_path(relative_path):
    """
    Ensures bundled files (api_key.txt, Persona, etc.) are found 
    whether running as a script or a standalone .app bundle.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_api_key():
    """Checks environment first, then the bundled api_key.txt."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    
    key_file = get_resource_path("api_key.txt")
    if os.path.exists(key_file):
        try:
            with open(key_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content: return content
        except:
            pass
    return ""

# --- CONFIGURATION ---
MODEL_NAME = "gemini-2.5-flash" 

def resolve_input_file(primary_name, fallback_name=None):
    """Finds personal input file first, falling back to example template if needed."""
    primary_path = get_resource_path(primary_name)
    if os.path.exists(primary_path):
        return primary_path
    if fallback_name:
        fallback_path = get_resource_path(fallback_name)
        if os.path.exists(fallback_path):
            return fallback_path
    return primary_path

PERSONA_FILE = resolve_input_file("Personafile.txt", "Personafile.example.txt")
KNOWLEDGE_BANK_FILE = resolve_input_file("KnowledgeBank.txt", "KnowledgeBank.example.txt")
RESUME_FILE = get_resource_path("Resume.docx")
CSS_FILE = get_resource_path("style.css")

# Output: Saves directly to your Desktop
OUTPUT_PDF = os.path.expanduser("~/Desktop/Tailored_Resume.pdf")
PATH_TO_WKHTMLTOPDF = '/usr/local/bin/wkhtmltopdf'

# --- 2. LOGIC ---

def read_text_file(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except:
            return ""
    return ""

def read_docx_file(filepath):
    if os.path.exists(filepath):
        try:
            doc = docx.Document(filepath)
            return "\n".join([p.text for p in doc.paragraphs])
        except: 
            return ""
    return ""

def extract_resume_smart(text, candidate_name=None):
    """Anchors to candidate header and stops before Phase 7 or other closing sections."""
    if not text: return ""
    
    # 1. Clean markdown artifacts
    clean_text = re.sub(r'^```markdown\n|```$', '', text, flags=re.IGNORECASE | re.MULTILINE).strip()
    
    # 2. Find start anchor: candidate name if provided, or first markdown header (# Candidate Name)
    start_match = None
    if candidate_name:
        escaped_name = re.escape(candidate_name)
        start_match = re.search(rf'#+\s*{escaped_name}', clean_text, re.IGNORECASE)
    
    if not start_match:
        # Fallback: anchor to first top-level or second-level Markdown heading
        start_match = re.search(r'^#{1,3}\s+[A-Za-z0-9]', clean_text, re.MULTILINE)
    
    if start_match:
        content = clean_text[start_match.start():]
        # 3. Kill Switch: Stop before Phase 7 or conversational summary
        end_match = re.search(r'#*\s*Phase\s*:?\s*7', content, re.IGNORECASE)
        if end_match:
            return content[:end_match.start()].strip()
        return content.strip()
    
    return clean_text

def apply_formatting_filters(text):
    """Removes AI brackets and fixes spacing."""
    if not text: return ""
    clean = text.replace('[', '').replace(']', '')
    clean = re.sub(r'\n\n\*', r'\n*', clean)
    clean = re.sub(r'\n(\*|-)', r'\n\n\1', clean)
    clean = clean.replace(' (Estimated)', '')
    return clean

def call_gemini_api(prompt, api_key):
    """Calls the gemini-2.5-flash model with backoff."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    retries = 5
    delays = [1, 2, 4, 8, 16]
    
    for i in range(retries):
        try:
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                candidates = result.get('candidates', [])
                if not candidates:
                    raise Exception("AI Response Blocked: Likely a safety filter trigger.")
                
                text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                if text: return text
                raise Exception("API returned valid structure but empty text.")
                
            elif response.status_code == 429:
                time.sleep(delays[i])
            else:
                error_body = response.text[:200]
                raise Exception(f"Google API Error ({response.status_code}): {error_body}")
                
        except Exception as e:
            if i == retries - 1:
                raise Exception(f"Failed after {retries} retries: {str(e)}")
            time.sleep(delays[i])
    return ""

def generate_resume_logic(jd, on_complete):
    """Main orchestration logic for background thread."""
    try:
        api_key = get_api_key()
        if not api_key: raise Exception("API Key Missing: Check api_key.txt.")

        if not os.path.exists(PATH_TO_WKHTMLTOPDF):
            raise Exception(f"System Error: wkhtmltopdf not found at {PATH_TO_WKHTMLTOPDF}")

        p_text = read_text_file(PERSONA_FILE)
        res_text = read_docx_file(RESUME_FILE)
        kb_text = read_text_file(KNOWLEDGE_BANK_FILE)
        
        if not p_text or not res_text:
            raise Exception("Input files (Persona or Resume) are missing or empty.")

        full_prompt = f"{p_text}\n\nSOURCES:\nKB: {kb_text}\nRES: {res_text}\n\nTARGET JD:\n{jd}"
        raw_response = call_gemini_api(full_prompt, api_key)
        
        resume_md = extract_resume_smart(raw_response)
        if not resume_md:
            raise Exception("Slicer Error: Could not parse resume content from AI response.")
            
        final_md = apply_formatting_filters(resume_md)

        html_body = markdown2.markdown(final_md)
        css_style = read_text_file(CSS_FILE)
        full_html = f"<html><head><meta charset='UTF-8'><style>{css_style}</style></head><body>{html_body}</body></html>"

        config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)
        pdfkit.from_string(full_html, OUTPUT_PDF, configuration=config)

        app.after(0, lambda: on_complete("Success! Saved to Desktop.", "green"))
        
    except Exception as e:
        traceback.print_exc()
        msg = str(e).strip()
        if not msg or msg == "None":
            msg = "Critical Internal Failure: Check Terminal Output."
        app.after(0, lambda: on_complete(f"Error: {msg}", "red"))

def start_thread():
    jd_input = textbox.get("1.0", "end-1c").strip()
    if not jd_input: 
        status_label.configure(text="Error: Paste a JD first.", text_color="red")
        return
        
    status_label.configure(text=f"AI strategizing ({MODEL_NAME})...", text_color="yellow")
    btn.configure(state="disabled")
    threading.Thread(target=lambda: generate_resume_logic(jd_input, _handle_finish), daemon=True).start()

def _handle_finish(msg, color):
    status_label.configure(text=msg, text_color=color)
    btn.configure(state="normal")

# --- 3. UI LAYOUT ---
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.geometry("500x550")
    app.title(f"Gemini Resume Slicer ({MODEL_NAME})")

    ctk.CTkLabel(app, text="Paste Job Description:", font=("Arial", 14, "bold")).pack(pady=(20, 5))
    textbox = ctk.CTkTextbox(app, width=450, height=350, font=("Arial", 12))
    textbox.pack(pady=10)

    btn = ctk.CTkButton(app, text="GENERATE TAILORED PDF", command=start_thread, font=("Arial", 13, "bold"), height=40)
    btn.pack(pady=10)

    status_label = ctk.CTkLabel(app, text="Ready", text_color="gray")
    status_label.pack(pady=5)

    app.mainloop()