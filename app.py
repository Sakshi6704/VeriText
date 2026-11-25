import streamlit as st
from pages import home, about, plagiarism_checker

def main():
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page == "Home":
        home.render_home()
    elif st.session_state.page == "About":
        about.render_about()
    elif st.session_state.page == "Plagiarism Checker":
        plagiarism_checker.render_plagiarism_checker()

# Corrected the condition to check if this is the main module
if __name__ == "__main__":
    main()
