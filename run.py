import streamlit as st
from backend.meme_generator import generate_meme
import os

# Ensure static directory exists
if not os.path.exists("frontend/static"):
    os.makedirs("frontend/static")

# Page configuration
st.set_page_config(
    page_title="MemeMind AI",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS with more AI style, reduced white space, and meme background
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDQwIDQwIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiM0NzNCREIiIGZpbGwtb3BhY2l0eT0iMC4xIj48cGF0aCBkPSJNMCAwaDQwdjQwSDB6TTIwIDIwaDIwdjIwSDIwek0wIDIwaDIwdjIwSDB6Ii8+PC9nPjwvZz48L3N2Zz4=');
        background-color: #0F0F1A;
        font-family: 'Exo 2', sans-serif;
        color: #e0e0ff;
    }
    
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0.5rem 1rem;
    }
    
    .main-header {
        background: linear-gradient(90deg, #3a1c71, #d76d77, #ffaf7b);
        background-size: 600% 600%;
        animation: gradientBG 10s ease infinite;
        color: white;
        padding: 1.5rem 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), 
                    0 0 30px rgba(103, 71, 205, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgdmlld0JveD0iMCAwIDYwIDYwIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNCNTc5REUiIGZpbGwtb3BhY2l0eT0iMC4yIj48cGF0aCBkPSJNMzYgMzRjMCAxLjEtLjkgMi0yIDJzLTItLjktMi0yIC45LTIgMi0yIDIgLjkgMiAyem0tMTggMGMwIDEuMS0uOSAyLTIgMnMtMi0uOS0yLTIgLjktMiAyLTIgMiAuOSAyIDJ6bTkgOGMtNS4zIDAtOS44LTMuOC0xMC44LTguOCAxLS4zIDEuOC0uMyAyLjkgMCAxLjMgNC40IDUuNCA3LjUgOS45IDcuNXM4LjYtMy4xIDkuOS03LjVjMS0uMyAxLjktLjMgMi45IDAtMS4xIDUtNS41IDguOC0xMC44IDguOHoiLz48L2c+PC9nPjwvc3ZnPg==');
        opacity: 0.2;
        z-index: 0;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3),
                     0 0 40px rgba(255, 255, 255, 0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    .input-container {
        background: rgba(30, 30, 50, 0.7);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3),
                    0 0 30px rgba(103, 71, 205, 0.2);
        margin-bottom: 1rem;
        border: 1px solid rgba(103, 71, 205, 0.3);
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(15, 15, 30, 0.7);
        color: #e0e0ff;
        border: 2px solid rgba(103, 71, 205, 0.7);
        border-radius: 10px;
        padding: 12px 15px;
        font-size: 16px;
        box-shadow: 0 0 15px rgba(103, 71, 205, 0.3);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #d76d77;
        box-shadow: 0 0 0 2px rgba(215, 109, 119, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #3a1c71, #d76d77, #ffaf7b);
        background-size: 200% auto;
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        border: none;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2),
                    0 0 30px rgba(103, 71, 205, 0.2);
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: pulse 2s infinite;
    }
    
    .stButton > button:hover {
        background-position: right center;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25),
                    0 0 30px rgba(103, 71, 205, 0.4);
    }
    
    .stSelectbox > div > div > div {
        background-color: rgba(15, 15, 30, 0.7);
        color: #e0e0ff;
        border: 2px solid rgba(103, 71, 205, 0.7);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    .meme-container {
        text-align: center;
        margin-top: 0.5rem;
        padding: 1.5rem;
        background: rgba(30, 30, 50, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3),
                    0 0 30px rgba(103, 71, 205, 0.2);
        animation: fadeIn 0.5s ease-in;
        border: 1px solid rgba(103, 71, 205, 0.3);
        height: 100%;
    }
    
    .download-btn {
        margin-top: 1rem;
    }
    
    .download-btn button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #0F0F1A;
        font-weight: 600;
    }
    
    .download-btn button:hover {
        background: linear-gradient(90deg, #00b8e6 0%, #83e58d 100%);
    }
    
    .instructions {
        background: rgba(30, 30, 50, 0.7);
        backdrop-filter: blur(10px);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3),
                    0 0 30px rgba(103, 71, 205, 0.2);
        margin-top: 1rem;
        border: 1px solid rgba(103, 71, 205, 0.3);
    }
    
    .instructions h3 {
        color: #d76d77;
        font-weight: 600;
        margin-bottom: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
    }
    
    .instructions h3::before {
        content: "🤖";
        margin-right: 0.5rem;
        font-size: 1.4rem;
    }
    
    .instructions ul {
        padding-left: 1.5rem;
        margin-bottom: 0;
    }
    
    .instructions li {
        margin-bottom: 0.5rem;
        position: relative;
    }
    
    .instructions li::before {
        content: "🔥";
        position: absolute;
        left: -1.5rem;
        top: 0;
    }
    
    .emoji-rotate {
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(10deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(103, 71, 205, 0.5); }
        70% { box-shadow: 0 0 0 10px rgba(103, 71, 205, 0); }
        100% { box-shadow: 0 0 0 0 rgba(103, 71, 205, 0); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .footer {
        text-align: center;
        margin-top: 1rem;
        padding: 0.5rem;
        font-size: 0.9rem;
        color: #888;
        background: rgba(30, 30, 50, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(103, 71, 205, 0.3);
    }
    
    .ai-badge {
        display: inline-block;
        background: linear-gradient(90deg, #3a1c71, #d76d77);
        color: white;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.5rem;
        vertical-align: middle;
        box-shadow: 0 0 10px rgba(103, 71, 205, 0.5);
    }
    
    /* Meme Grid */
    .meme-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .meme-grid-item {
        background: rgba(15, 15, 30, 0.7);
        border-radius: 8px;
        overflow: hidden;
        transition: all 0.3s ease;
        position: relative;
        aspect-ratio: 1/1;
        cursor: pointer;
    }
    
    .meme-grid-item:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(103, 71, 205, 0.5);
    }
    
    .meme-grid-item img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .meme-placeholder {
        background: rgba(30, 30, 50, 0.7);
        padding: 2rem 1rem;
        border-radius: 12px;
        text-align: center;
        height: 100%;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 2px dashed rgba(103, 71, 205, 0.5);
    }
    
    .placeholder-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        opacity: 0.7;
        animation: pulse 2s infinite;
    }
    
    /* Floating particles */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    
    .particle {
        position: absolute;
        width: 10px;
        height: 10px;
        background: rgba(103, 71, 205, 0.3);
        border-radius: 50%;
        animation: float-particle 15s infinite linear;
    }
    
    @keyframes float-particle {
        0% { transform: translateY(0) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 30, 0.7);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(103, 71, 205, 0.7);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(215, 109, 119, 0.7);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .input-container, .meme-container, .instructions {
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Floating AI particles background
st.markdown("""
    <div class="particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header with AI futuristic styling
st.markdown("""
    <div class="main-header">
        <h1>MemeMind AI <span class="emoji-rotate">🤖</span></h1>
        <p>The ultimate AI-powered meme factory your friends won't believe exists!</p>
    </div>
""", unsafe_allow_html=True)

# Two-column layout for inputs and outputs - made more compact
col1, col2 = st.columns([2, 3], gap="small")

with col1:
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # User input text with AI badge
    st.markdown("""
        <div style='margin-bottom: 0.5rem;'>
            <span style='font-weight: 600; font-size: 1.1rem;'>Enter your meme idea</span>
            <span class='ai-badge'>AI POWERED</span>
        </div>
    """, unsafe_allow_html=True)
    
    text_input = st.text_input(
        "",
        value="AI fails at hackathon",
        placeholder="e.g., 'When the code works on your machine but not in production'"
    )
    
    # Output format selection with futuristic style
    st.markdown("<div style='margin-top: 1rem; margin-bottom: 0.5rem;'><strong>Meme Format:</strong></div>", unsafe_allow_html=True)
    output_format = st.selectbox(
        "",
        ["1:1 (Square - Instagram)", "4:3 (Landscape - Twitter/X)"],
        index=0
    )
    format_value = "1:1" if output_format == "1:1 (Square - Instagram)" else "4:3"
    
    # Generate meme button with AI styling
    st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
    generate_button = st.button("🔥 GENERATE EPIC MEME 🔥")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick meme templates - visual grid
    st.markdown('<div class="instructions">', unsafe_allow_html=True)
    st.markdown("<h3>Trending Meme Ideas</h3>", unsafe_allow_html=True)
    
    # Meme template grid
    st.markdown("""
        <div class="meme-grid">
            <div class="meme-grid-item">
                <img src="https://via.placeholder.com/100x100/0F0F1A/FFFFFF?text=AI+Fail" alt="AI Fail">
            </div>
            <div class="meme-grid-item">
                <img src="https://via.placeholder.com/100x100/0F0F1A/FFFFFF?text=404" alt="404 Not Found">
            </div>
            <div class="meme-grid-item">
                <img src="https://via.placeholder.com/100x100/0F0F1A/FFFFFF?text=WFH" alt="Work From Home">
            </div>
            <div class="meme-grid-item">
                <img src="https://via.placeholder.com/100x100/0F0F1A/FFFFFF?text=Bugs" alt="Programming Bugs">
            </div>
            <div class="meme-grid-item">
                <img src="https://via.placeholder.com/100x100/0F0F1A/FFFFFF?text=Monday" alt="Monday Blues">
            </div>
            <div class="meme-grid-item">
                <img src="https://via.placeholder.com/100x100/0F0F1A/FFFFFF?text=Coffee" alt="Coffee Addiction">
            </div>
            <div class="meme-grid-item">
                <img src="https://via.placeholder.com/100x100/0F0F1A/FFFFFF?text=Deadline" alt="Deadline Panic">
            </div>
            <div class="meme-grid-item">
                <img src="https://via.placeholder.com/100x100/0F0F1A/FFFFFF?text=Sleep" alt="No Sleep">
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Compact instructions
    st.markdown('<div class="instructions">', unsafe_allow_html=True)
    st.markdown("<h3>How It Works</h3>", unsafe_allow_html=True)
    st.markdown("""
        <ul>
            <li>Type your meme concept or select from trending ideas</li>
            <li>Choose your format (square or landscape)</li>
            <li>Hit the generate button and watch our AI work its magic</li>
            <li>Download & share your creation to become a meme lord</li>
        </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Meme display area
with col2:
    if generate_button:
        with st.spinner("🧠 Neural networks firing... Creating your meme masterpiece!"):
            try:
                meme_path = generate_meme(text_input, output_format=format_value)
                full_meme_path = os.path.join("frontend", meme_path)
                
                if os.path.exists(full_meme_path):
                    st.markdown("<div class='meme-container'>", unsafe_allow_html=True)
                    
                    # AI generation badge
                    st.markdown("""
                        <div style="background: rgba(103, 71, 205, 0.3); display: inline-block; padding: 0.3rem 0.7rem; 
                                    border-radius: 20px; margin-bottom: 1rem; font-size: 0.8rem; border: 1px solid rgba(103, 71, 205, 0.5);">
                            <span style="vertical-align: middle;">✨ AI GENERATED</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the generated meme
                    st.image(full_meme_path, caption="", use_column_width=True)
                    
                    # Download and share buttons
                    with open(full_meme_path, "rb") as file:
                        col_down, col_share = st.columns([1, 1])
                        
                        with col_down:
                            st.markdown("<div class='download-btn'>", unsafe_allow_html=True)
                            st.download_button(
                                label="⬇️ Download",
                                data=file,
                                file_name="mememind_creation.jpg",
                                mime="image/jpeg",
                                key="download_button"
                            )
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col_share:
                            st.markdown("""
                                <div style="margin-top: 1rem;">
                                    <button style="background: linear-gradient(90deg, #3a1c71, #d76d77); color: white; border: none; 
                                             padding: 0.75rem 1.5rem; border-radius: 10px; width: 100%; cursor: pointer; font-weight: 600;">
                                        🚀 SHARE
                                    </button>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    # Meme stats
                    st.markdown("""
                        <div style="display: flex; justify-content: space-between; margin-top: 1rem; 
                                  background: rgba(15, 15, 30, 0.5); padding: 0.5rem; border-radius: 8px;">
                            <div style="text-align: center;">
                                <div style="font-size: 0.8rem; opacity: 0.7;">HUMOR RATING</div>
                                <div style="font-size: 1.2rem; font-weight: 600;">9.7/10</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 0.8rem; opacity: 0.7;">GENERATION TIME</div>
                                <div style="font-size: 1.2rem; font-weight: 600;">0.8s</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 0.8rem; opacity: 0.7;">MEME POWER</div>
                                <div style="font-size: 1.2rem; font-weight: 600;">LEGENDARY</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("😕 Oops! We couldn't generate your meme. Please try a different prompt or try again later.")
            except Exception as e:
                st.error(f"😞 Error generating meme: {str(e)}")
    else:
        # Placeholder with AI tech feel
        st.markdown("""
            <div class="meme-placeholder">
                <div class="placeholder-icon">🤖</div>
                <p style="font-size: 1.2rem; color: #d76d77; font-weight: 500; margin-bottom: 1rem;">
                    AI Meme Generator Ready
                </p>
                <p style="color: #8a8aa3; font-size: 0.9rem;">
                    Enter your meme idea and click the generate button to unleash the AI memery!
                </p>
                <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap;">
                    <span style="background: rgba(103, 71, 205, 0.3); padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">#AI</span>
                    <span style="background: rgba(103, 71, 205, 0.3); padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">#Memes</span>
                    <span style="background: rgba(103, 71, 205, 0.3); padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">#MachineLearning</span>
                    <span style="background: rgba(103, 71, 205, 0.3); padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">#Funny</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer with cyberpunk style
st.markdown("""
    <div class="footer">
        <p>© 2025 MemeMind AI • Powered by Neural Networks and Human Creativity • v3.7.0</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)