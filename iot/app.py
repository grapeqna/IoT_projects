from flask import Flask, render_template
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)

@app.route("/")
def combine_images():
    img0 = Image.open("static/0.jpg")
    img1 = Image.open("static/1.jpg")
    img2 = Image.open("static/2.jpg")

    combined_img = Image.new("RGB", (450, 300))

    combined_img.paste(img0, (0, 0))
    combined_img.paste(img1.resize((150, 150)), (300, 0))
    combined_img.paste(img2.resize((150, 150)), (300, 150))

    enh = ImageEnhance.Brightness(combined_img)
    bright_img = enh.enhance(2.0)

    bright_img.save("static/fin.jpg") 
    return render_template("index.html", path="fin.jpg")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
