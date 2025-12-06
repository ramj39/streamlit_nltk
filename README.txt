# Streamlit NLTK Text Extractor

This project is a Streamlit application that extracts sentences or lines from uploaded text files (TXT, PDF, DOCX) or pasted text. 
It allows users to select ranges of sentences for display, and optionally convert them into speech using gTTS (Google Text-to-Speech).

---

## Features
- Upload multi-format files (TXT, PDF, DOCX).
- Paste text directly into the app.
- Automatic sentence tokenization using NLTK.
- Select start and end indices to view specific ranges.
- Optional speech synthesis with gTTS (MP3 playback and download).
- Simple, browser-based interface powered by Streamlit.

---

## Requirements
Install dependencies in your environment:
pip install streamlit nltk gtts pandas PyPDF2 python-docx
If using conda, you may also need
conda install -c conda-forge nltk

---

## Setup
1. Clone or copy the project files into a folder (e.g., `E:\streamlit_nltk`).
2. Ensure your environment is active:


3. Run the app:
streamlit run app.py
