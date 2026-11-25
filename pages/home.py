import streamlit as st

def render_home():
    # Set page title and icon (optional)
    st.set_page_config(page_title="Plagiarism Checker", page_icon="📝")

    # Centered title and image
    st.markdown(
        """
        <div style='text-align: center;'>
            <h1 style='color: #4CAF50;'>Welcome to the Plagiarism Checker 🕵️‍♂️</h1>
            <img src='https://cdn-icons-png.flaticon.com/512/2889/2889676.png' width='200'/>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")

    # Introduction with emoji and nice formatting
    st.markdown("""
    <div style="text-align: center;">
        <h3>📄 Compare documents | 🔍 Detect similarity | ✅ Get plagiarism score</h3>
        <p style="font-size: 16px; line-height: 1.6;">
            This powerful tool helps you compare two text files and calculate the <strong>plagiarism percentage</strong> 
            based on content similarity.<br><br>
            Just upload your `.txt`,Direct text or Pdf documents and get an instant analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

   # Button layout
    col1, col2, col3= st.columns(3)
    with col1:
        st.button("📊 Go to Plagiarism Checker", key="go_to_upload", on_click=lambda: st.session_state.update({"page": "Plagiarism Checker"}))
    with col2:
        st.button("ℹ️ Go to About Page", key="go_to_about", on_click=lambda: st.session_state.update({"page": "About"}))
    