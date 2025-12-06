import streamlit as st
import io
import nltk
import PyPDF2
from docx import Document
import pandas as pd
from gtts import gTTS
import base64

# Ensure punkt is available every run
nltk.download("punkt", quiet=True)

st.title("Multi‑Format Text Extractor with Speech")

uploaded_file = st.file_uploader(
    "Upload a file (.txt, .pdf, .docx, .csv)",
    type=["txt", "pdf", "docx", "csv"]
)

def safe_decode(raw_bytes: bytes) -> str:
    """Try multiple encodings for robustness."""
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return raw_bytes.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("utf-8", errors="replace")

def speak_and_download(selected_text: str):
    """Convert text to speech, play audio, and provide download link."""
    if not selected_text.strip():
        st.warning("No text selected for speech.")
        return
    tts = gTTS(selected_text)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)

    # Play audio
    st.audio(audio_bytes, format="audio/mp3")

    # Provide download link
    b64 = base64.b64encode(audio_bytes.read()).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="speech.mp3">Download MP3</a>'
    st.markdown(href, unsafe_allow_html=True)

if uploaded_file is not None:
    text = ""

    # Handle TXT
    if uploaded_file.type == "text/plain":
        raw_bytes = uploaded_file.read()
        text = safe_decode(raw_bytes)

    # Handle PDF
    elif uploaded_file.type == "application/pdf":
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

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

    # Line mode only
    lines = text.splitlines()
    st.write(f"Detected {len(lines)} lines.")

    start_idx = st.number_input("Start line", 1, len(lines), 1)
    end_idx = st.number_input("End line", start_idx, len(lines), min(start_idx+9, len(lines)))
    selected = lines[start_idx-1:end_idx]

    st.subheader(f"Lines {start_idx} to {end_idx}:")
    for i, s in enumerate(selected, start=start_idx):
        st.write(f"{i}. {s}")

    if st.button("Speak Selected Lines"):
        speak_and_download("\n".join(selected))
else:
    st.info("Upload a file to extract lines.")

st.info("Developed by Subramanian Ramajayam")
st.snow()
