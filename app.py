import streamlit as st
import os
from PyPDF2 import PdfReader
from utils.summarizer import summarize_text
from utils.ppt_generator import create_ppt

# Page config
st.set_page_config(
    page_title="🧠 Research Paper Summarizer",
    layout="wide",
    page_icon="📄"
)

# Custom styles
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: white;
        }
        h1, h2, h3 {
            color: #f9fafb;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
        }
        .reportview-container .main footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Title and instructions
st.markdown("""
    # 📄 Research Paper Summarizer
    Upload a research paper PDF and get a bullet-point summary with a downloadable PowerPoint presentation.
""")

# Upload PDF
pdf_file = st.file_uploader("📎 Upload a research paper (PDF only)", type=["pdf"])

if pdf_file:
    st.success("✅ PDF uploaded successfully!")

    # Read and extract text
    with st.spinner("📖 Extracting text from PDF..."):
        pdf = PdfReader(pdf_file)
        raw_text = ""
        for page in pdf.pages:
            raw_text += page.extract_text()

    # Summarize
    with st.spinner("🤖 Generating summary using AI..."):
        summary = summarize_text(raw_text)

    # Display summary
    st.markdown("## 📝 Summary")
    summary_html = "<br><br>".join([f"• {point}" for point in summary.split("\n") if point.strip()])
    st.markdown(
        f"""
        <div style='background-color: #ffffff; color: #000000; padding: 20px; border-radius: 10px; font-size: 18px; line-height: 1.7; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);'>
            {summary_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create PowerPoint
    with st.spinner("📽 Creating PowerPoint presentation..."):
        ppt_path = create_ppt(summary)

    # Download button
    with open(ppt_path, "rb") as file:
        st.download_button(
            label="⬇️ Download PPT",
            data=file,
            file_name="Research_Summary.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
