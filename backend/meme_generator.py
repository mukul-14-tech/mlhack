from transformers import pipeline  # Note: We'll keep this for potential future use, but it’s not critical now
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
import requests
import io
from openai import OpenAI

# Initialize OpenAI client with environment variable
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Template paths with thematic keywords
TEMPLATES_DIR = "backend/templates"
TEMPLATES = {
    "drake": {
        "path": os.path.join(TEMPLATES_DIR, "drake_hotline.jpg"),
        "tone": "satirical",
        "layout": "two_panel",
        "themes": ["contrast",  "preference"]
    },
    "success_kid": {
        "path": os.path.join(TEMPLATES_DIR, "success_kid.jpg"),
        "tone": "positive",
        "layout": "single",
        "themes": ["victory", "achievement"]
    },
    "distracted_boyfriend": {
        "path": os.path.join(TEMPLATES_DIR, "distracted_boyfriend.jpg"),
        "tone": "humorous",
        "layout": "three_panel",
        "themes": ["distraction", "ignoring", "chasing"]
    },
    "balloon_interruption": {
        "path": os.path.join(TEMPLATES_DIR, "balloon_interruption.jpg"),
        "tone": "humorous",
        "layout": "two_panel",
        "themes": ["interruption", "distraction"]
    },
    "spongebob_transformation": {
        "path": os.path.join(TEMPLATES_DIR, "spongebob_transformation.jpg"),
        "tone": "positive",
        "layout": "five_panel",
        "themes": ["transformation", "progression", "growth"]
    },
    "classroom_rage": {
        "path": os.path.join(TEMPLATES_DIR, "classroom_rage.jpg"),
        "tone": "satirical",
        "layout": "two_panel",
        "themes": ["rage", "frustration", "failure"]
    },
    "doge_muscle": {
        "path": os.path.join(TEMPLATES_DIR, "doge_muscle.jpg"),
        "tone": "humorous",
        "layout": "two_panel",
        "themes": ["transformation", "comparison", "strength"]
    },
    "incredibles_disapproval": {
        "path": os.path.join(TEMPLATES_DIR, "incredibles_disapproval.jpg"),
        "tone": "satirical",
        "layout": "two_panel",
        "themes": ["disapproval", "realization", "disappointment"]
    },
    "winnie_pooh": {
        "path": os.path.join(TEMPLATES_DIR, "winnie_pooh.jpg"),
        "tone": "positive",
        "layout": "two_panel",
        "themes": ["self-improvement", "smart", "realization"]
    }
}

def analyze_text(text):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are an expert in analyzing text to determine emotional tone and themes for meme generation."},
                {"role": "user", "content": f"Analyze the following text and determine its emotional tone (satirical, humorous, positive) and specific themes (e.g., distraction, transformation, rage, victory). Return the result as a JSON object with 'tone' and 'themes' keys: {text}"}
            ],
            max_tokens=100,
            temperature=0.3
        )
        analysis = response.choices[0].message.content.strip()
        # Parse the JSON response
        import json
        result = json.loads(analysis)
        tone = result["tone"].lower()
        themes = result["themes"]
        print(f"Analyzed text: '{text}' | Detected tone: {tone} | Themes: {themes}")
        return tone, themes
    except Exception as e:
        print(f"Error with OpenAI analysis: {e}")
        # Fallback to simple keyword-based analysis
        text_lower = text.lower()
        satirical_keywords = ["fail", "lose", "mess", "wrong", "disappoint", "rage", "scandal", "crisis", "collapse"]
        humorous_keywords = ["distract", "ignore", "forget", "walk", "turn", "funny", "joke", "muscle", "lol"]
        positive_keywords = ["win", "success", "great", "awesome", "transform", "smart", "victory", "achievement", "breakthrough"]
        
        if any(keyword in text_lower for keyword in satirical_keywords):
            tone = "satirical"
        elif any(keyword in text_lower for keyword in humorous_keywords):
            tone = "humorous"
        elif any(keyword in text_lower for keyword in positive_keywords):
            tone = "positive"
        else:
            tone = "humorous"

        themes = []
        if "distract" in text_lower or "ignore" in text_lower or "chasing" in text_lower:
            themes.append("distraction")
        if "interrupt" in text_lower:
            themes.append("interruption")
        if "transform" in text_lower or "grow" in text_lower or "progress" in text_lower:
            themes.append("transformation")
        if "rage" in text_lower or "frustrat" in text_lower:
            themes.append("rage")
        if "compare" in text_lower or "strength" in text_lower or "muscle" in text_lower:
            themes.append("comparison")
        if "disapprove" in text_lower or "disappoint" in text_lower or "realize" in text_lower:
            themes.append("disapproval")
        if "smart" in text_lower or "improve" in text_lower:
            themes.append("self-improvement")
        if "contrast" in text_lower or "prefer" in text_lower:
            themes.append("contrast")
        if "win" in text_lower or "victory" in text_lower or "achieve" in text_lower:
            themes.append("victory")
        if "fail" in text_lower or "crisis" in text_lower or "scandal" in text_lower:
            themes.append("failure")

        print(f"Analyzed text: '{text}' | Detected tone: {tone} | Themes: {themes} | (Fallback analysis)")
        return tone, themes

def generate_caption_with_openai(text, tone, layout):
    prompt = f"Analyze the following text and determine its emotional tone (satirical, humorous, positive) and specific themes (e.g., distraction, transformation, rage, victory, interruption, self-improvement). Focus on the most dominant emotion and avoid overgeneralizing to 'distraction'. Return the result as a JSON object with 'tone' and 'themes' keys: {text}"
    if layout == "two_panel":
        prompt += "Create a two-part caption (e.g., 'When X fails / When Y succeeds')."
    elif layout == "three_panel":
        prompt += "Create a three-part caption (e.g., 'X / Ignoring Y / Chasing Z')."
    elif layout == "five_panel":
        prompt += "Create a five-part caption showing progression (e.g., 'Step 1: X / Step 2: Y / ...')."
    else:  # single
        prompt += "Create a single celebratory caption (e.g., 'X wins!')."
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a creative assistant that generates funny and contextually appropriate meme captions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        caption_text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI Chat API: {e}")
        # Fallback to simple generation
        words = text.split()
        subject = words[0].lower() if words else "it"
        if layout == "two_panel":
            action = words[1].lower() if len(words) > 1 else "fails"
            opposite_action = "succeeds" if "fail" in action else "wins" if "lose" in action else "works"
            return [f"When {subject} {action}", f"When {subject} {opposite_action}"]
        elif layout == "three_panel":
            action = words[1].lower() if len(words) > 1 else "distracts"
            secondary = words[2].lower() if len(words) > 2 else "something"
            return [subject.capitalize(), f"Ignoring {action}", f"Chasing {secondary}"]
        elif layout == "five_panel":
            return [f"Step 1: {subject}", f"Step 2: Trying", f"Step 3: Growing", f"Step 4: Stronger", f"Step 5: Success"]
        else:
            return [f"{subject.capitalize()} wins!"]

    # Post-process captions
    if layout == "two_panel":
        captions = caption_text.split("/")
        if len(captions) != 2:
            words = text.split()
            subject = words[0].lower() if words else "it"
            action = words[1].lower() if len(words) > 1 else "fails"
            opposite_action = "succeeds" if "fail" in action else "wins" if "lose" in action else "works"
            captions = [f"When {subject} {action}", f"When {subject} {opposite_action}"]
    elif layout == "three_panel":
        captions = caption_text.split("/")
        if len(captions) != 3:
            words = text.split()
            subject = words[0].capitalize() if words else "Someone"
            action = words[1].lower() if len(words) > 1 else "distracts"
            secondary = words[2].lower() if len(words) > 2 else "something"
            captions = [subject, f"Ignoring {action}", f"Chasing {secondary}"]
    elif layout == "five_panel":
        captions = caption_text.split("/")
        if len(captions) != 5:
            words = text.split()
            subject = words[0].lower() if words else "it"
            captions = [f"Step 1: {subject}", f"Step 2: Trying", f"Step 3: Growing", f"Step 4: Stronger", f"Step 5: Success"]
    else:
        captions = [caption_text]
        if not captions[0]:
            words = text.split()
            subject = words[0].capitalize() if words else "Victory"
            captions = [f"{subject} wins!"]

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
    tone, themes = analyze_text(text)
    
    # Select the best template based on tone and themes
    best_template = None
    max_theme_match = 0
    for template_name, template_info in TEMPLATES.items():
        if template_info["tone"] != tone:
            continue
        # Count matching themes
        theme_match = sum(1 for theme in themes if theme in template_info["themes"])
        if theme_match > max_theme_match and os.path.exists(template_info["path"]):
            max_theme_match = theme_match
            best_template = template_info
    
    # If no suitable template is found, use OpenAI DALL·E to generate one
    if best_template is None:
        # Default to a generic template for the tone if no themes match
        available_templates = [t for t in TEMPLATES.values() if t["tone"] == tone and os.path.exists(t["path"])]
        if available_templates:
            best_template = available_templates[0]
        else:
            # Use DALL·E to generate a context-specific template
            layout = "two_panel" if tone == "satirical" else "three_panel" if tone == "humorous" else "single"
            if "transformation" in themes:
                layout = "five_panel"
            try:
                prompt = f"A {tone} meme template with a {layout} layout, styled like a classic internet meme, featuring clean and simple characters, emphasizing the theme of {', '.join(themes) if themes else tone}, no pre-existing text"
                response = openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    n=1,
                    response_format="url"
                )
                image_url = response.data[0].url
                response = requests.get(image_url)
                img = Image.open(io.BytesIO(response.content)).convert("RGB")
                # Save with a unique name based on tone and themes
                theme_suffix = "_".join(themes) if themes else tone
                new_template_path = os.path.join(TEMPLATES_DIR, f"{tone}_{theme_suffix}_generated.jpg")
                img.save(new_template_path, format="JPEG", quality=95)
                best_template = {
                    "path": new_template_path,
                    "tone": tone,
                    "layout": layout,
                    "themes": themes
                }
                print(f"Generated new template at {new_template_path}")
            except Exception as e:
                print(f"Error with DALL·E API: {e}")
                # Fallback to success_kid as a last resort
                best_template = TEMPLATES["incredibles_disapproval"]
                if not os.path.exists(best_template["path"]):
                    raise FileNotFoundError("Default template 'incredible_disapproal.jpg' not found. Please ensure templates are in backend/templates/.")
    
    template_path = best_template["path"]
    layout = best_template["layout"]

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

    captions = generate_caption_with_openai(text, tone, layout)
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