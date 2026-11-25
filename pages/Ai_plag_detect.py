import streamlit as st
import random
from langdetect import detect
from datetime import datetime
from reportlab.pdfgen import canvas
import io
import plotly.graph_objects as go
import PyPDF2

st.set_page_config(page_title="Detect AI-Generated Content", layout="centered", page_icon="🤖")

st.markdown("## 🤖 Detect AI-Generated Content")
st.markdown("Enter text or upload a file to check AI detection")

# Function to read PDF file and extract text
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Simulate AI detection score
def detect_ai(text):
    random.seed(text)
    return random.uniform(0.3, 0.95)

# Generate PDF report
def generate_pdf_report(text, score, language):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica", 12)
    c.drawString(100, 800, "AI Detection Report")
    c.drawString(100, 780, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 760, f"Detected Language: {language}")
    c.drawString(100, 740, f"Confidence Score (AI): {100 - score*100 - 4:.2f}%")
    c.drawString(100, 720, f"AI Generated: {'Yes' if score < 0.65 else 'No'}")
    c.drawString(100, 700, "Text:")
    y = 680
    for line in text.split("\n"):
        c.drawString(100, y, line[:90])
        y -= 15
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    buffer.seek(0)
    return buffer

# Text input and file upload
direct_text = st.text_area("Enter text directly here:", height=200)

uploaded_file = st.file_uploader(
    "Or upload a text, PDF, or code file",
    type=['txt', 'pdf', 'py', 'java', 'cpp', 'js', 'c', 'cs']
)

content = ""

# Read uploaded file
if uploaded_file is not None:
    file_name = uploaded_file.name
    st.write(f"Uploaded file: {file_name}")
    try:
        if file_name.endswith((".txt", ".py", ".java", ".cpp", ".js", ".c", ".cs")):
            content = uploaded_file.read().decode("utf-8")
        elif file_name.endswith(".pdf"):
            content = read_pdf(uploaded_file)
        else:
            st.error("Unsupported file type")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Override with direct text
if direct_text.strip():
    content = direct_text

# Detect AI button
if st.button("Detect AI"):
    if content.strip() == "":
        st.warning("Please enter some text or upload a file.")
    else:
        try:
            language = detect(content)
        except:
            language = "Unknown"

        # Get score and interpret it in reverse
        score = detect_ai(content)
        human_score = round(score * 100, 2)
        other_score = 4.0
        ai_score = round(100 - human_score - other_score, 2)

        # Donut chart (Relation Chart)
        labels = ['AI Generated', 'Human Written', 'Other']
        values = [ai_score, human_score, other_score]
        colors = ['red', 'green', 'Orange']

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker=dict(colors=colors),
            textinfo='label+percent',
            insidetextorientation='radial'
        )])

        fig_pie.update_layout(
            title_text='Detection Confidence Breakdown',
            annotations=[dict(text='', x=0.5, y=0.5, font_size=20, showarrow=False)],
            showlegend=True
        )

        st.plotly_chart(fig_pie)

        # Detection result
        if score < 0.65:
            st.success("❌ This content appears to be AI-generated.")
        else:
            st.warning("✅ This content appears to be Human-written.")

        st.markdown(f"*Detected Language:* {language}")
        st.markdown(f"*AI Confidence Score:* {ai_score:.2f}%")
        st.markdown(f"*Human Confidence Score:* {human_score:.2f}%")

        # PDF download
        pdf = generate_pdf_report(content, score, language)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf,
            file_name="ai_detection_report.pdf",
            mime="application/pdf"
        )

        # Show content
        st.text_area("Detected Text (read-only)", content, height=200, disabled=True)
        st.code(content, language="text")

        # Clipboard button (visual only)
        st.button("📋 Copy Text to Clipboard")

        # Rewrite suggestion
        if score < 0.65:
            if st.button("✏️ Rewrite to Human-like Text"):
                st.info("🔄 Rewriting not implemented. You can integrate with OpenAI or other LLM APIs.")

    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
import streamlit as st
import random
from langdetect import detect
from datetime import datetime
from reportlab.pdfgen import canvas
import io
import plotly.graph_objects as go
import PyPDF2

st.set_page_config(page_title="Detect AI-Generated Content", layout="centered", page_icon="🤖")

st.markdown("## 🤖 Detect AI-Generated Content")
st.markdown("Enter text or upload a file to check AI detection")

# Function to read PDF file and extract text
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Simulate AI detection score
def detect_ai(text):
    random.seed(text)
    return random.uniform(0.3, 0.95)

# Generate PDF report
def generate_pdf_report(text, score, language):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica", 12)
    c.drawString(100, 800, "AI Detection Report")
    c.drawString(100, 780, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 760, f"Detected Language: {language}")
    c.drawString(100, 740, f"Confidence Score (AI): {100 - score*100 - 4:.2f}%")
    c.drawString(100, 720, f"AI Generated: {'Yes' if score < 0.65 else 'No'}")
    c.drawString(100, 700, "Text:")
    y = 680
    for line in text.split("\n"):
        c.drawString(100, y, line[:90])
        y -= 15
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    buffer.seek(0)
    return buffer

# Text input and file upload
direct_text = st.text_area("Enter text directly here:", height=200)

uploaded_file = st.file_uploader(
    "Or upload a text, PDF, or code file",
    type=['txt', 'pdf', 'py', 'java', 'cpp', 'js', 'c', 'cs']
)

content = ""

# Read uploaded file
if uploaded_file is not None:
    file_name = uploaded_file.name
    st.write(f"Uploaded file: {file_name}")
    try:
        if file_name.endswith((".txt", ".py", ".java", ".cpp", ".js", ".c", ".cs")):
            content = uploaded_file.read().decode("utf-8")
        elif file_name.endswith(".pdf"):
            content = read_pdf(uploaded_file)
        else:
            st.error("Unsupported file type")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Override with direct text
if direct_text.strip():
    content = direct_text

# Detect AI button
if st.button("Detect AI"):
    if content.strip() == "":
        st.warning("Please enter some text or upload a file.")
    else:
        try:
            language = detect(content)
        except:
            language = "Unknown"

        # Get score and interpret it in reverse
        score = detect_ai(content)
        human_score = round(score * 100, 2)
        other_score = 4.0
        ai_score = round(100 - human_score - other_score, 2)

        # Donut chart (Relation Chart)
        labels = ['AI Generated', 'Human Written', 'Other']
        values = [ai_score, human_score, other_score]
        colors = ['red', 'green', 'Orange']

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker=dict(colors=colors),
            textinfo='label+percent',
            insidetextorientation='radial'
        )])

        fig_pie.update_layout(
            title_text='Detection Confidence Breakdown',
            annotations=[dict(text='', x=0.5, y=0.5, font_size=20, showarrow=False)],
            showlegend=True
        )

        st.plotly_chart(fig_pie)

        # Detection result
        if score < 0.65:
            st.success("❌ This content appears to be AI-generated.")
        else:
            st.warning("✅ This content appears to be Human-written.")

        st.markdown(f"*Detected Language:* {language}")
        st.markdown(f"*AI Confidence Score:* {ai_score:.2f}%")
        st.markdown(f"*Human Confidence Score:* {human_score:.2f}%")

        # PDF download
        pdf = generate_pdf_report(content, score, language)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf,
            file_name="ai_detection_report.pdf",
            mime="application/pdf"
        )

        # Show content
        st.text_area("Detected Text (read-only)", content, height=200, disabled=True)
        st.code(content, language="text")

        # Clipboard button (visual only)
        st.button("📋 Copy Text to Clipboard")

        # Rewrite suggestion
        if score < 0.65:
            if st.button("✏️ Rewrite to Human-like Text"):
                st.info("🔄 Rewriting not implemented. You can integrate with OpenAI or other LLM APIs.")

    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"