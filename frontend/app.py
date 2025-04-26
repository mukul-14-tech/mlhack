from flask import Flask, render_template, request, send_file
from backend.meme_generator import generate_meme
import os

app = Flask(__name__, template_folder="templates", static_folder="frontend/static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")
        output_format = request.form.get("output_format", "1:1")
        if topic:
            meme_path = generate_meme(topic, output_format=output_format)
            return render_template("index.html", meme_url=f"/{meme_path}")
    return render_template("index.html", meme_url=None)

if __name__ == "__main__":
    app.run(debug=True)