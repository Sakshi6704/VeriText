import streamlit as st

def render_about():
    st.set_page_config(page_title="About - Plagiarism Checker", page_icon="ℹ️")

    # About Header without the image
    st.markdown("""
        <div style="text-align: center; animation: fadeIn 1.2s ease-in-out;">
            <h1 style='color:#4CAF50;'>About the Plagiarism Checker 📝</h1>
        </div>
        <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Section with background image and text overlay
    st.markdown("""
    <div style="
        background-image: url('C:/Sakshi Docs/ai_text_detector_project/image1.webp');
        background-size: cover;
        background-position: center;
        padding: 60px 30px;
        border-radius: 12px;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    ">
        <h2 style="font-size: 30px; margin-bottom: 20px;">🎯 Ideal For</h2>
        <ul style="font-size: 18px; line-height: 1.8;">
            <li><strong>Teachers and Professors 📚</strong></li>
            <li><strong>Students verifying their work before submission ✍️</strong></li>
            <li><strong>Writers ensuring originality of content ✨</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Plagiarism explanation
    st.markdown("""
    <div style="font-size: 17px; line-height: 1.7;">
        <h3>🔍 How It Works</h3>
        <p>This tool leverages state-of-the-art text comparison techniques to detect potential plagiarism in documents:</p>
        <ul>
            <li><strong>TF-IDF (Term Frequency-Inverse Document Frequency)</strong>: Identifies how important a word is in a document relative to a collection of documents.</li>
            <li><strong>Cosine Similarity</strong>: Measures the cosine of the angle between two text vectors, representing document similarity.</li>
        </ul>
        <p>The tool computes a <strong>plagiarism percentage</strong> to help you understand how much one document overlaps with another.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Back to home button
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"

