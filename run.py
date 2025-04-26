# run.py
import streamlit as st
from backend.meme_generator import generate_meme
import os

# Ensure static directory exists
if not os.path.exists("frontend/static"):
    os.makedirs("frontend/static")

# Custom CSS for a white, AI-driven Supermeme.ai-like design
st.set_page_config(page_title="MemeMind AI", layout="wide")
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput > div > div > input {
        background-color: #f9f9f9;
        color: #333333;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        border: none;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    h1 {
        color: #4CAF50;
        text-align: center;
        font-size: 36px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stSelectbox > div > div > div {
        background-color: #f9f9f9;
        color: #333333;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 5px;
    }
    .meme-container {
        text-align: center;
        margin-top: 20px;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("MemeMind AI - Your AI Meme Generator")

# Logo (optional, add a custom image if desired)
st.markdown("<div style='text-align:center;'><img src='https://via.placeholder.com/150x50.png?text=MemeMind+AI' alt='MemeMind AI Logo'></div>", unsafe_allow_html=True)

# Text input
text_input = st.text_input("Enter a topic, headline, or idea (e.g., 'AI fails at hackathon', 'Boss distracts team')", "AI fails at hackathon")

# Output format selection
output_format = st.selectbox("Select output format for social media", ["1:1 (Square)", "4:3 (Landscape)"], index=0)
format_value = "1:1" if output_format == "1:1 (Square)" else "4:3"

# Generate button
if st.button("Generate Meme"):
    with st.spinner("Crafting your meme with AI intelligence..."):
        meme_path = generate_meme(text_input, output_format=format_value)
        full_meme_path = os.path.join("frontend", meme_path)
        if os.path.exists(full_meme_path):
            st.markdown("<div class='meme-container'>", unsafe_allow_html=True)
            st.image(full_meme_path, caption="Your AI-Generated Meme", use_container_width=True)
            with open(full_meme_path, "rb") as file:
                st.download_button(
                    label="Download Meme",
                    data=file,
                    file_name="meme.jpg",
                    mime="image/jpeg",
                    key="download_button"
                )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("Error: Could not generate the meme. Please try again.")

# Instructions
st.write("""
- Enter any topic, news headline, or idea, and MemeMind AI will create a perfect meme for you!
- Supports multiple templates and custom AI-generated images.
- Choose your preferred output format for social media sharing.
- Powered by advanced AI for humor, satire, and relevance!
""")