# frontend/app.py
from flask import Flask, render_template, request, send_file
from backend import analyze_topic, generate_meme, overlay_text
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"]
        analysis = analyze_topic(topic)
        meme_data = generate_meme(analysis)
        meme_path = overlay_text(meme_data, "frontend/static/output_meme.jpg")
        return render_template("index.html", meme_url="/static/output_meme.jpg")
    return render_template("index.html", meme_url=None)

if __name__ == "__main__":
    app.run(debug=True)