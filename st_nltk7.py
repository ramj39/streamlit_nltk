import streamlit as st
import io
import nltk
from nltk.tokenize import sent_tokenize
import PyPDF2
from docx import Document
import pandas as pd
from gtts import gTTS
import base64

# Ensure punkt is available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

st.title("Multi‑Format Text Extractor with Speech")

uploaded_file = st.file_uploader(
    "Upload a file (.txt, .pdf, .docx, .csv)",
    type=["txt", "pdf", "docx", "csv"]
)

def safe_decode(raw_bytes: bytes) -> str:
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return raw_bytes.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("utf-8", errors="replace")

if uploaded_file is not None:
    text = ""

    # Handle TXT
    if uploaded_file.type == "text/plain":
        raw_bytes = uploaded_file.read()
        text = safe_decode(raw_bytes)

    # Handle PDF
    elif uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])

    # Handle DOCX
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])

    # Handle CSV
    elif uploaded_file.type == "text/csv":
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)
        text = "\n".join(df.astype(str).apply(" ".join, axis=1))

    if not text.strip():
        st.warning("No extractable text found.")
        st.stop()

    # Toggle between sentence mode and line mode
    mode = st.radio("Choose extraction mode:", ["By Sentences", "By Lines"])

    if mode == "By Sentences":
        sentences = sent_tokenize(text)
        st.write(f"Detected {len(sentences)} sentences.")

        start_idx = st.number_input("Start sentence", 1, len(sentences), 1)
        end_idx = st.number_input("End sentence", start_idx, len(sentences), min(start_idx+9, len(sentences)))
        selected = sentences[start_idx-1:end_idx]

        st.subheader(f"Sentences {start_idx} to {end_idx}:")
        for i, s in enumerate(selected, start=start_idx):
            st.write(f"{i}. {s}")

    else:  # Line mode
        lines = text.splitlines()
        st.write(f"Detected {len(lines)} lines.")

        start_idx = st.number_input("Start line", 1, len(lines), 1)
        end_idx = st.number_input("End line", start_idx, len(lines), min(start_idx+9, len(lines)))
        selected = lines[start_idx-1:end_idx]

        st.subheader(f"Lines {start_idx} to {end_idx}:")
        for i, s in enumerate(selected, start=start_idx):
            st.write(f"{i}. {s}")
        if st.button("Speak Selected"):
            selected_text = "\n".join(selected)
st.info("developed by Subramanian Ramajayam")
st.snow()
