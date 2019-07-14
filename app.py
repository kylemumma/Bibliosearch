from flask import Flask, render_template, Response
from forms import ImageForm
from text_recognition import Text_Recognition
from screenshot import ScreenshotCamera

app = Flask(__name__)

app.config["SECRET_KEY"] = 'e3e78f4328134a6308fa595609ea174e'

screenshotCamera = ScreenshotCamera()
tr = Text_Recognition()

@app.route('/', methods=["GET", "POST"])
def hello_world():
    form = ImageForm()

    target_word = form.target_word.data
    rotate_image = form.rotate_image.data

    if(target_word != None and
        rotate_image != None):
        screenshotCamera.destroy()
        screenshotCamera.start(target_word, rotate_image)

    return render_template("index.html", form=form)

if(__name__ == "__main__"):
    app.run(debug=True)