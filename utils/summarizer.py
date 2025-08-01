# utils/summarizer.py

import streamlit as st
from transformers import pipeline
import textwrap

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def chunk_text(text, max_words=400):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

def summarize_text(text):
    summarizer = load_summarizer()
    chunks = list(chunk_text(text))
    
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=180, min_length=40, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    
    return "\n\n".join(summaries)
