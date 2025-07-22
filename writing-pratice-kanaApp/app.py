import streamlit as st
import requests
import random
from PIL import Image
from io import BytesIO
import base64

# === Global State ===
if "word_list" not in st.session_state:
    st.session_state.word_list = []
if "current_word" not in st.session_state:
    st.session_state.current_word = None
if "english_sentence" not in st.session_state:
    st.session_state.english_sentence = ""
if "grading_result" not in st.session_state:
    st.session_state.grading_result = None

# === Config ===
API_BASE_URL = "http://localhost:5000"
GROUP_ID = 1  # This would be dynamically set per user/group

# === Initialization ===
@st.cache_data
def fetch_word_group():
    response = requests.get(f"{API_BASE_URL}/api/groups/{GROUP_ID}/raw")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to load word group.")
        return []

st.title("✍️ Language Writing Practice")

# === Load word list on init ===
if not st.session_state.word_list:
    st.session_state.word_list = fetch_word_group()

# === Sentence Generator ===
def generate_sentence_prompt(word):
    return f"""
Generate a Japanese sentence using the word: {word}.
- Grammar level: JLPT N5.
- Only use the given word or words from this group.
- Keep it short and simple.
- Also return an English translation.
"""

def mock_llm_response(word):
    """Placeholder for LLM backend. Replace with actual call."""
    examples = {
        "car": ("これは新しい車です。", "This is a new car."),
        "book": ("私は本を読みます。", "I read a book."),
        "new": ("新しい本があります。", "There is a new book.")
    }
    return examples.get(word.lower(), ("ラーメンを食べます。", "I eat ramen."))

# === Setup State ===
st.subheader("1. Generate a Sentence")

if st.button("Generate Sentence"):
    chosen = random.choice(st.session_state.word_list)
    st.session_state.current_word = chosen["english"]
    jp, en = mock_llm_response(chosen["english"])
    st.session_state.english_sentence = en
    st.session_state.japanese_sentence = jp
    st.session_state.grading_result = None

if st.session_state.english_sentence:
    st.markdown(f"**English Sentence:** {st.session_state.english_sentence}")
    st.markdown("✍️ Write this sentence in Japanese by hand, then upload an image.")

    uploaded_image = st.file_uploader("Upload your handwritten sentence", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Your Submission", use_column_width=True)

    if st.button("Submit for Review") and uploaded_image is not None:
        # Save image locally or send directly to grading system
        image_bytes = uploaded_image.read()

        # Simulate Grading System API (replace with actual call)
        grading_result = mock_grading_system(image_bytes, st.session_state.english_sentence)
        st.session_state.grading_result = grading_result

# === Grading Display ===
if st.session_state.grading_result:
    st.subheader("📝 Grading Result")
    st.markdown(f"**Grade:** {st.session_state.grading_result['grade']}")
    st.markdown(f"**Transcription:** {st.session_state.grading_result['transcription']}")
    st.markdown(f"**Translation:** {st.session_state.grading_result['translation']}")
    st.markdown(f"**Feedback:** {st.session_state.grading_result['feedback']}")
