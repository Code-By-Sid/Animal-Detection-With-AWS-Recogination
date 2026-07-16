from flask import Flask, render_template, request, redirect
import requests
import base64

app = Flask(__name__)

API = "https://ayx78z4kq7.execute-api.ap-south-1.amazonaws.com/default/"


@app.route("/")
def home():

    try:

        response = requests.get(API + "/animals")

        data = response.json()

        images = data.get("images", [])

        counts = data.get("animalCount", {})

    except Exception as e:

        print(e)

        images = []

        counts = {}

    return render_template(
        "index.html",
        images=images,
        counts=counts
    )


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["image"]

    image_bytes = file.read()

    encoded = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    body = {

        "filename": file.filename,

        "image": encoded

    }

    requests.post(

        API + "/upload",

        json=body

    )

    return redirect("/")


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )