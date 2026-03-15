import markdown2
import pdfkit
import os
import re

# --- Constants ---
PATH_TO_WKHTMLTOPDF = '/usr/local/bin/wkhtmltopdf'
CSS_FILE = "style.css"
OUTPUT_PDF = "Full_Resume_Test.pdf"

# REAL WORLD EXPORT (With the AI's current quirks)
test_markdown = """
## JEREMY SPAUNHURST | MBA
[559-708-3339] | [jeremy@spaunhurst.com] | [linkedin.com/in/jeremyspaunhurst] | [Austin, TX]

---
### EXECUTIVE SUMMARY
Senior Program Director driving operational excellence in large-scale data programs that empower machine learning and AI initiatives. My focus is on using operational data to improve efficiency, reduce risks, and lead diverse teams in implementing smarter processes for continuous improvement. I ensure cross-functional teams work in sync, optimizing data workflows across global operations to deliver high-quality insights and speed up product development.
---
### EXECUTIVE EXPERIENCE
**Guinn Partners** | Program Director | 2021 – Present (Estimated)
* **Capacity Governance & Team Restructuring**: Directed capacity governance efforts, introducing clear performance standards and systemic feedback loops to restructure the software team for growth, improving overall team productivity.
* **Operational Intelligence Systems**: Designed and deployed integrated project management dashboards (JIRA, Asana, Tableau) for macro-level resource allocation and real-time project health, enabling proactive risk identification across workflows.
* **Cross-Matrix Prioritization**: Led workback schedule development and task prioritization across interdependent teams, aligning resource availability with strategic milestones for consistent project delivery.

**Extreme Arts and Science** | Senior Project Manager | 2018 – 2021 (Estimated)
* **Data-Driven Client Insights**: Increased client engagement and white paper downloads by 5.3x (from 300 to 1,600 click-throughs) by identifying data trends and implementing proactive homepage content recommendations for Microsoft.

* **Large-Scale Data Labeling & Content Operations**: Managed the production of 60 webinar videos from nearly 1,000 hours of footage, overseeing content tagging for AI model training and coordinating distributed onshore and offshore editing teams.

* **Data Workflow Optimization**: Built a Frame.io tracking system for video production feedback, significantly reducing revision cycles and accelerating delivery timelines for large-scale client content.

* **Risk Mitigation & Stakeholder Trust**: Prioritized transparency with NVIDIA on a $1M proposal, immediately correcting a $15,000 financial error and strengthening long-term client trust and relationship.
---
### EDUCATION & CERTIFICATIONS 
* **MBA - Program Management**, Louisiana State University (GPA 4.0)
* **Lean Six Sigma Black Belt** (Credential ID 2F7fdDQ26D)
* **Certified Scrum Master** (Credential ID 001387948)
"""

print("1. Cleaning AI artifacts and converting to HTML...")

# THE FILTERS (Updated for your latest export)
# 1. Kill Brackets
clean_text = test_markdown.replace('[', '').replace(']', '')

# 2. Fix the AI's weird double-spacing between bullets (The "Extreme Arts" fix)
clean_text = re.sub(r'\n\n\*', r'\n*', clean_text)

# 3. Ensure a clean gap before ALL bullet types (* or -) so they don't mash into titles
clean_text = re.sub(r'\n(\*|-)', r'\n\n\1', clean_text)

# 4. Remove the "(Estimated)" artifact to keep titles clean
clean_text = clean_text.replace(' (Estimated)', '')

html_content = markdown2.markdown(clean_text)

css = ""
if os.path.exists(CSS_FILE):
    with open(CSS_FILE, "r") as f:
        css = f.read()

full_html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><style>{css}</style></head><body>{html_content}</body></html>"

options = {
    'page-size': 'Letter',
    'margin-top': '0.4in',
    'margin-right': '0.4in',
    'margin-bottom': '0.4in',
    'margin-left': '0.4in',
    'encoding': "UTF-8",
}

print("2. Generating Full PDF...")
try:
    config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)
    pdfkit.from_string(full_html, OUTPUT_PDF, options=options, configuration=config)
    print(f"✅ Success! Open {OUTPUT_PDF} to see the fixed layout.")
except Exception as e:
    print(f"❌ Error: {e}")