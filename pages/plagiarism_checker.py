import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
from io import BytesIO
import nltk
from nltk.corpus import stopwords
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from langdetect import detect
import time

nltk.download("stopwords")
nltk.download('punkt')
nltk.download('wordnet')

# Initialize session state for history if not exists
if 'history' not in st.session_state:
    st.session_state['history'] = []

custom_stopwords = {
    "hindi": {"और", "है", "था", "के", "को", "में", "की", "से", "का", "पर"},
    "marathi": {"आहे", "आणि", "मध्ये", "है", "साठी", "की", "चा", "च्या"},
    "gujarati": {"અને", "છે", "મા", "હે", "ને", "થી", "કે", "પર", "ના"}
}

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def detect_language(text):
    try:
        lang_code = detect(text)
        return lang_code
    except:
        return "english"

def get_stopwords(lang_code):
    try:
        return stopwords.words(lang_code)
    except:
        if lang_code in custom_stopwords:
            return list(custom_stopwords[lang_code])
        st.warning(f"No stopword list found for '{lang_code}'. Using English as fallback.")
        return stopwords.words("english")

def calculate_plagiarism(text1, text2, lang_code):
    stop_words = get_stopwords(lang_code)
    tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tfidf_vectorizer.fit_transform([text1, text2])
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_matrix[0][0] * 100

def get_highlighted_text(text1, text2):
    matcher = SequenceMatcher(None, text1, text2)
    highlighted_text1, highlighted_text2 = "", ""
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            highlighted_text1 += f"<span style='background-color: lightgreen;'>{text1[i1:i2]}</span>"
            highlighted_text2 += f"<span style='background-color: lightgreen;'>{text2[j1:j2]}</span>"
        else:
            highlighted_text1 += text1[i1:i2]
            highlighted_text2 += text2[j1:j2]
    return highlighted_text1, highlighted_text2

def generate_report(score):
    unique = 100 - score
    report = f"Plagiarism Report\n\nPlagiarized Content: {score:.2f}%\nUnique Content: {unique:.2f}%"
    return report

def remove_plagiarized_sections(source, target):
    matcher = SequenceMatcher(None, source, target)
    cleaned = ""
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != 'equal':
            cleaned += target[j1:j2]
    return cleaned

def create_cleaned_pdf(text, filename="cleaned_document.pdf"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    lines = text.split('\n')

    for line in lines:
        if y <= 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, line[:120])
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer

def render_plagiarism_checker():
    st.set_page_config(page_title="Plagiarism Checker", page_icon="🕵️‍♂️")
    st.title("📊 Multilingual Plagiarism Checker")

    st.markdown("""
    <style>
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: #00cc44; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

    # 🌟 SHOW LANGUAGE SELECTION ALWAYS 🌟
    lang_choice = st.selectbox(
        "Select Language for Stopwords Handling",
        options=["auto-detect", "english", "hindi", "marathi", "gujarati"],
        index=0
    )

    num_files = st.slider("How many documents do you want to upload?", 2, 5)
    input_type = st.selectbox("Choose input method", ["Text Files", "Direct Text", "PDF Files"])
    text_list = []

    for i in range(num_files):
        st.markdown(f"### Document {i + 1}")
        if input_type == "Text Files":
            file = st.file_uploader(f"Upload file {i + 1} (.txt)", type="txt", key=f"file_{i}")
            if file:
                text_list.append(file.read().decode("utf-8"))
        elif input_type == "Direct Text":
            text = st.text_area(f"Enter text for Document {i + 1}", key=f"text_{i}")
            text_list.append(text)
        elif input_type == "PDF Files":
            file = st.file_uploader(f"Upload PDF file {i + 1}", type="pdf", key=f"pdf_{i}")
            if file:
                text_list.append(extract_text_from_pdf(file))

    if len(text_list) == num_files and all(text.strip() for text in text_list):
        progress = st.progress(0)
        for percent_complete in range(0, 30, 10):
            time.sleep(0.1)
            progress.progress(percent_complete)

        # detect lang only if auto-detect
        if lang_choice == "auto-detect":
            detected_lang = detect_language(text_list[0])
            st.info(f"Auto Detected Language: {detected_lang.title()}")
        else:
            detected_lang = lang_choice

        similarity_scores = []
        comparisons = [(i, j) for i in range(num_files - 1) for j in range(i + 1, num_files)]

        for idx, (i, j) in enumerate(comparisons):
            score = calculate_plagiarism(text_list[i], text_list[j], detected_lang)
            similarity_scores.append(score)

        for percent_complete in range(30, 80, 10):
            time.sleep(0.1)
            progress.progress(percent_complete)

        st.subheader("🔍 Plagiarism Results")
        total_score = sum(similarity_scores) / len(similarity_scores)
        unique = 100 - total_score

        st.session_state['history'].append({
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'plagiarized': total_score,
            'unique': unique
        })

        fig = go.Figure(go.Pie(
            values=[total_score, unique],
            labels=["Plagiarized Content", "Unique Content"],
            hole=0.6,
            marker=dict(colors=["#ff4d4d", "#3adb76"]),
            textinfo='label+percent'
        ))
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### 🔴 {total_score:.2f}% Plagiarized Content")
        with col2:
            st.markdown(f"### 🟢 {unique:.2f}% Unique Content")

        st.markdown("#### 📄 Document Comparisons:")
        for idx, (i, j) in enumerate(comparisons):
            st.markdown(f"- Document {i + 1} vs Document {j + 1}: {similarity_scores[idx]:.2f}% plagiarized")

        report_content = generate_report(total_score)
        st.download_button("📥 Download Report", data=report_content, file_name="plagiarism_report.txt", mime="text/plain")

        st.subheader("📑 Matched Text Highlight")
        for idx, (i, j) in enumerate(comparisons):
            highlight1, highlight2 = get_highlighted_text(text_list[i], text_list[j])
            st.markdown(f"#### Document {i+1} vs Document {j+1}")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div style='padding:10px;border:1px solid #ccc;height:300px;overflow:auto;'>{highlight1}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='padding:10px;border:1px solid #ccc;height:300px;overflow:auto;'>{highlight2}</div>", unsafe_allow_html=True)

        st.subheader("🧹 Remove Plagiarized Content (Optional)")
        remove_option = st.radio("Do you want to remove plagiarized content from documents?", ["No", "Yes"])
        if remove_option == "Yes":
            cleaned_texts = []
            for i, j in comparisons:
                cleaned = remove_plagiarized_sections(text_list[i], text_list[j])
                cleaned_texts.append(cleaned)

            st.success("Plagiarized content removed.")

            st.markdown("#### ✨ Cleaned Documents Content")
            for idx, cleaned_text in enumerate(cleaned_texts):
                st.markdown(
                    f"<div style='padding:10px;border:1px solid #ccc;height:300px;overflow:auto;background-color:black;color:#00cc44;font-family:monospace;'>{cleaned_text}</div>",
                    unsafe_allow_html=True
                )

            st.download_button(
                "📄 Download Cleaned Documents (Text)",
                data="\n\n".join(cleaned_texts),
                file_name="cleaned_documents.txt",
                mime="text/plain"
            )

        if st.session_state['history']:
            st.subheader("🕒 Previous Session History")
            for idx, entry in enumerate(st.session_state['history'][:-1][::-1], start=1):
                st.markdown(f"{idx}. [{entry['timestamp']}] - Plagiarized: {entry['plagiarized']:.2f}%, Unique: {entry['unique']:.2f}%")

        for percent_complete in range(80, 101, 10):
            time.sleep(0.1)
            progress.progress(percent_complete)

    else:
        st.info("Please upload all documents to perform the check.")

    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"

if __name__ == "__main__":
    render_plagiarism_checker()