from pathlib import Path
import streamlit as st


def load_theme():
    css = Path("assets/style.css").read_text()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )
