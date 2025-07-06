# ---- AI Flashcard Creator App ----

import streamlit as st
import spacy
import docx
import PyPDF2
import re

# -------------------- Page Settings --------------------
st.set_page_config(page_title="AI Flashcard Creator", layout="wide")
st.title("📚 AI-Powered Flashcard Creator")
st.markdown("Upload a file (TXT, PDF, or DOCX) and get smart flashcards from its content!")

# -------------------- Load spaCy Model --------------------
@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

nlp = load_nlp_model()

# -------------------- File Reader --------------------
def read_file(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    elif file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        return ""

# -------------------- Flashcard Generator --------------------
import re

def generate_flashcards(text):
    """
    Generate simple flashcards using rule-based pattern matching.
    """
    flashcards = []
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence.split()) < 4:
            continue

        if ' is ' in sentence:
            parts = sentence.split(' is ', 1)
            question = f"What is {parts[0].strip()}?"
            answer = sentence
            flashcards.append((question, answer))
        elif ' are ' in sentence:
            parts = sentence.split(' are ', 1)
            question = f"What are {parts[0].strip()}?"
            answer = sentence
            flashcards.append((question, answer))
        elif ' refers to ' in sentence:
            parts = sentence.split(' refers to ', 1)
            question = f"What does {parts[0].strip()} refer to?"
            answer = sentence
            flashcards.append((question, answer))
        elif ' means ' in sentence:
            parts = sentence.split(' means ', 1)
            question = f"What does {parts[0].strip()} mean?"
            answer = sentence
            flashcards.append((question, answer))

    return flashcards


# -------------------- Streamlit UI --------------------
uploaded_file = st.file_uploader("📁 Upload a file", type=["txt", "pdf", "docx"])

if uploaded_file:
    file_text = read_file(uploaded_file)

    if file_text.strip():
        st.success("✅ File uploaded and read successfully!")

        # Preview first few lines
        st.subheader("📄 File Preview")
        st.write(file_text[:500] + "...")

        # Generate flashcards
        flashcards = generate_flashcards(file_text)

        if flashcards:
            st.subheader("🧠 Generated Flashcards")
            for i, (q, a) in enumerate(flashcards):
                with st.expander(f"Q{i+1}: {q}"):
                    st.write(f"**Answer:** {a}")
        else:
            st.warning("⚠️ Couldn't generate flashcards. Try another file.")

    else:
        st.warning("⚠️ No text found in the uploaded file.")