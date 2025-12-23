import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="PDF Summary", layout="wide")

if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'info' not in st.session_state:
    st.session_state.info = {}


def get_history():
    try:
        response = requests.get(f"{BACKEND_URL}/history", timeout=5)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        st.error(f"Failed to fetch history: {e}")
        return []


def get_audio_bytes(filename):
    try:
        url = f"{BACKEND_URL}/audio/{filename}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
        return None
    except Exception:
        return None


def upload_file(file):
    files = {"file": (file.name, file, "application/pdf")}
    try:
        with st.spinner("Analyzing..."):
            response = requests.post(f"{BACKEND_URL}/upload", files=files)

        if response.status_code == 200:
            data = response.json()
            st.session_state.summary = data['summary']
            st.session_state.info = {
                "filename": data['filename'],
                "tokens": data.get('tokens_used', 0),
                "cost": data.get('cost_usd', 0.0),
                "audio": data.get('audio_filename')
            }
            st.success("Analysis & Voiceover complete!")
        else:
            detail = response.json().get('detail', 'Unknown error')
            st.error(f"Error: {detail}")
    except Exception as e:
        st.error(f"Connection error: {e}")


with st.sidebar:
    st.title("🕒 History")
    history = get_history()
    for doc in history:
        if st.button(f"📄 {doc['filename']}", key=doc['id'], use_container_width=True):
            st.session_state.summary = doc['summary']
            st.session_state.info = {
                "filename": doc['filename'],
                "tokens": doc.get('tokens_used', 0),
                "cost": doc.get('cost_usd', 0.0),
                "audio": doc.get('audio_filename')
            }
            st.rerun()

st.title("📄 PDF Summary AI")
uploaded_file = st.file_uploader("Upload PDF (max 50MB)", type="pdf")

if uploaded_file and st.button("Analyze Document", type="primary"):
    upload_file(uploaded_file)

st.divider()

if st.session_state.summary:
    info = st.session_state.info
    st.subheader(f"Results for: {info.get('filename', 'Doc')}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Status", "Completed", border=True)
    col2.metric("Tokens Used", f"{info.get('tokens', 0):,}", border=True)
    col3.metric("Est. Cost", f"${info.get('cost', 0):.5f}", border=True)

    audio_file = info.get('audio')
    if audio_file:
        st.write("### 🎧 Listen to Summary")
        audio_bytes = get_audio_bytes(audio_file)
        if audio_bytes:
            st.audio(audio_bytes, format='audio/mp3')
        else:
            st.warning("Audio file not found on server (maybe deleted?)")

    st.markdown("### Summary")
    st.markdown(st.session_state.summary)