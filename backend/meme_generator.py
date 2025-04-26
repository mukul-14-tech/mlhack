from transformers import pipeline
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
import requests
import io
from openai import OpenAI
import torch

# Initialize sentiment analyzer
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Initialize OpenAI client with environment variable
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Placeholder for LLaMA API (e.g., Together AI or Replicate)
LLAMA_API_URL = "https://api.together.ai/v1/chat/completions"
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

# Template paths
TEMPLATES_DIR = "backend/templates"
TEMPLATES = {
    "drake": {"path": os.path.join(TEMPLATES_DIR, "drake_hotline.jpg"), "tone": "satirical", "layout": "two_panel"},
    "success_kid": {"path": os.path.join(TEMPLATES_DIR, "success_kid.jpg"), "tone": "positive", "layout": "single"},
    "distracted_boyfriend": {"path": os.path.join(TEMPLATES_DIR, "distracted_boyfriend.jpg"), "tone": "humorous", "layout": "three_panel"},
    "balloon_interruption": {"path": os.path.join(TEMPLATES_DIR, "balloon_interruption.jpg"), "tone": "humorous", "layout": "two_panel"},
    "spongebob_transformation": {"path": os.path.join(TEMPLATES_DIR, "spongebob_transformation.jpg"), "tone": "positive", "layout": "five_panel"},
    "classroom_rage": {"path": os.path.join(TEMPLATES_DIR, "classroom_rage.jpg"), "tone": "satirical", "layout": "two_panel"},
    "doge_muscle": {"path": os.path.join(TEMPLATES_DIR, "doge_muscle.jpg"), "tone": "humorous", "layout": "two_panel"},
    "incredibles_disapproval": {"path": os.path.join(TEMPLATES_DIR, "incredibles_disapproval.jpg"), "tone": "satirical", "layout": "two_panel"},
    "winnie_pooh": {"path": os.path.join(TEMPLATES_DIR, "winnie_pooh.jpg"), "tone": "positive", "layout": "two_panel"}
}

def analyze_text(text):
    sentiment = sentiment_analyzer(text)[0]
    text_lower = text.lower()
    
    # Enhanced tone detection with contextual keywords for news and general text
    satirical_keywords = ["fail", "lose", "mess", "wrong", "disappoint", "rage", "scandal", "crisis", "collapse"]
    humorous_keywords = ["distract", "ignore", "forget", "walk", "turn", "funny", "joke", "muscle", "lol"]
    positive_keywords = ["win", "success", "great", "awesome", "transform", "smart", "victory", "achievement", "breakthrough"]
    
    if any(keyword in text_lower for keyword in satirical_keywords) or sentiment["label"] == "NEGATIVE":
        tone = "satirical"
    elif any(keyword in text_lower for keyword in humorous_keywords):
        tone = "humorous"
    elif any(keyword in text_lower for keyword in positive_keywords) or sentiment["label"] == "POSITIVE":
        tone = "positive"
    else:
        tone = "humorous"  # Default to humorous for neutral cases
    
    print(f"Analyzed text: '{text}' | Detected tone: {tone} | Sentiment: {sentiment}")
    return tone

def generate_caption_with_llama(text, tone):
    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"Generate a {tone} meme caption for the topic: {text}. "
    if tone == "satirical":
        prompt += "Create a two-part caption showing contrast (e.g., 'When X fails / When Y succeeds')."
    elif tone == "positive":
        prompt += "Create a single celebratory caption (e.g., 'X wins!')."
    else:  # humorous
        prompt += "Create a three-part caption for a distracted boyfriend meme (e.g., 'X / Ignoring Y / Chasing Z')."
    
    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(LLAMA_API_URL, headers=headers, json=data)
        response.raise_for_status()
        caption_text = response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error with LLaMA API: {e}")
        print(f"Response text: {e.response.text if e.response else 'No response text'}")
        # Fallback to simple generation
        words = text.split()
        subject = words[0].lower() if words else "it"
        if tone == "satirical":
            action = words[1].lower() if len(words) > 1 else "fails"
            opposite_action = "succeeds" if "fail" in action else "wins" if "lose" in action else "works"
            return [f"When {subject} {action}", f"When {subject} {opposite_action}"]
        elif tone == "positive":
            return [f"{subject.capitalize()} wins!"]
        else:
            action = words[1].lower() if len(words) > 1 else "distracts"
            secondary = words[2].lower() if len(words) > 2 else "something"
            return [subject.capitalize(), f"Ignoring {action}", f"Chasing {secondary}"]
    
    # Post-process captions
    if tone == "satirical":
        captions = caption_text.split("/")
        if len(captions) != 2:
            words = text.split()
            subject = words[0].lower() if words else "it"
            action = words[1].lower() if len(words) > 1 else "fails"
            opposite_action = "succeeds" if "fail" in action else "wins" if "lose" in action else "works"
            captions = [f"When {subject} {action}", f"When {subject} {opposite_action}"]
    elif tone == "positive":
        captions = [caption_text]
        if not captions[0]:
            words = text.split()
            subject = words[0].capitalize() if words else "Victory"
            captions = [f"{subject} wins!"]
    else:  # humorous
        captions = caption_text.split("/")
        if len(captions) != 3:
            words = text.split()
            subject = words[0].capitalize() if words else "Someone"
            action = words[1].lower() if len(words) > 1 else "distracts"
            secondary = words[2].lower() if len(words) > 2 else "something"
            captions = [subject, f"Ignoring {action}", f"Chasing {secondary}"]
    
    return [cap.strip() for cap in captions]

def detect_text_regions(image_path, layout):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h > 5000:  # Filter small regions
            regions.append((x, y, w, h))
    
    regions = sorted(regions, key=lambda r: r[2] * r[3], reverse=True)
    
    if layout == "two_panel":
        regions = sorted(regions, key=lambda r: r[1])
        if len(regions) >= 2:
            return [(regions[0][0], regions[0][1], regions[0][2], regions[0][3]),
                    (regions[-1][0], regions[-1][1], regions[-1][2], regions[-1][3])]
    elif layout == "three_panel":
        regions = sorted(regions, key=lambda r: r[0])
        if len(regions) >= 3:
            return [(regions[i][0], regions[i][1], regions[i][2], regions[i][3]) for i in range(3)]
    elif layout == "five_panel":
        regions = sorted(regions, key=lambda r: r[1])
        if len(regions) >= 5:
            return [(regions[i][0], regions[i][1], regions[i][2], regions[i][3]) for i in range(5)]
    else:
        if regions:
            return [regions[0]]
    
    img_height, img_width = img.shape[:2]
    if layout == "two_panel":
        return [(img_width // 2, 10, img_width // 2 - 20, 50),
                (img_width // 2, img_height - 60, img_width // 2 - 20, 50)]
    elif layout == "three_panel":
        return [(10, img_height - 60, img_width // 3 - 20, 50),
                (img_width // 3 + 10, img_height - 60, img_width // 3 - 20, 50),
                (2 * img_width // 3 + 10, img_height - 60, img_width // 3 - 20, 50)]
    elif layout == "five_panel":
        panel_width = img_width // 5
        return [(i * panel_width + 10, img_height - 60, panel_width - 20, 50) for i in range(5)]
    else:
        return [(10, img_height // 2, img_width - 20, 50)]

def generate_meme(text, output_format="1:1"):
    tone = analyze_text(text)
    # Select template based on tone with preference for existing files
    available_templates = [t for t in TEMPLATES.values() if t["tone"] == tone and os.path.exists(t["path"])]
    template = available_templates[0] if available_templates else next((t for t in TEMPLATES.values() if os.path.exists(t["path"])), TEMPLATES["success_kid"])
    template_path = template["path"]
    layout = template["layout"]

    # Fallback to OpenAI DALL·E if no matching template exists or file is missing
    if not os.path.exists(template_path) or not any(t["tone"] == tone for t in TEMPLATES.values()):
        try:
            response = openai_client.images.generate(
                model="dall-e-3",
                prompt=f"A {tone} meme template with {layout} layout, styled like a classic internet meme, featuring clean and simple characters, emphasizing a {tone} theme, no pre-existing text",
                size="1024x1024",
                n=1,
                response_format="url"
            )
            image_url = response.data[0].url
            response = requests.get(image_url)
            img = Image.open(io.BytesIO(response.content)).convert("RGB")
            # Save with a unique name based on tone and layout as JPEG
            new_template_path = os.path.join(TEMPLATES_DIR, f"{tone}_{layout}_generated.jpg")
            img.save(new_template_path, format="JPEG", quality=95)
            template_path = new_template_path
            print(f"Generated new template at {new_template_path}")
        except Exception as e:
            print(f"Error with DALL·E API: {e}")
            # Fallback to default template if DALL·E fails
            template_path = TEMPLATES["success_kid"]["path"]
            layout = TEMPLATES["success_kid"]["layout"]
            img = Image.open(template_path).convert("RGB")

    else:
        img = Image.open(template_path).convert("RGB")

    draw = ImageDraw.Draw(img)

    # Load font
    initial_font_size = 40
    try:
        font = ImageFont.truetype("impact.ttf", initial_font_size)
    except:
        font = ImageFont.load_default()
        initial_font_size = 12

    # Detect text regions using computer vision
    text_regions = detect_text_regions(template_path, layout)

    # Dynamic text placement
    def fit_text(text, max_width, current_font, current_font_size):
        font = current_font
        font_size = current_font_size
        while True:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            if text_width < max_width or font_size <= 10:
                return font
            font_size -= 2
            try:
                font = ImageFont.truetype("impact.ttf", font_size)
            except:
                font = ImageFont.load_default()
                break

    captions = generate_caption_with_llama(text, tone)
    for i, (region, caption) in enumerate(zip(text_regions, captions)):
        x, y, w, h = region
        font = fit_text(caption.upper(), w, font, initial_font_size)
        bbox = draw.textbbox((0, 0), caption.upper(), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x_pos = x + (w - text_width) // 2
        y_pos = y + (h - text_height) // 2
        draw.text((x_pos, y_pos), caption.upper(), font=font, fill="white", stroke_width=2, stroke_fill="black")

    # Adjust image for output format
    if output_format == "4:3":
        new_width = int(img.height * 4 / 3)
        new_img = Image.new("RGB", (new_width, img.height), "white")
        offset = (new_width - img.width) // 2
        new_img.paste(img, (offset, 0))
        img = new_img

    # Save and return the path as JPEG
    output_dir = "frontend/static"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, "output_meme.jpg")
    img.save(output_path, format="JPEG", quality=95)
    return os.path.join("static", "output_meme.jpg")