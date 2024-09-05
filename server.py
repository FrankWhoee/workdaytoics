from flask import Flask, request, render_template, redirect
app = Flask(__name__)

from src.convert import convert

import os

port = os.getenv("PORT", default=5000)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file:
            cal = convert(file.read()).to_ics()
            return render_template("index.html", cal=cal)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=port, host="0.0.0.0")