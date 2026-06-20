from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

uploaded_files = []

@app.route("/")
def home():
    return render_template(
        "index.html",
        files=uploaded_files
    )

@app.route("/upload", methods=["POST"])
def upload():

    employee_name = request.form["employee_name"]
    uploaded_file = request.files["file"]

    if employee_name and uploaded_file:

        filepath = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.filename
        )

        uploaded_file.save(filepath)

        uploaded_files.append({
            "employee": employee_name,
            "filename": uploaded_file.filename
        })

    return render_template(
        "index.html",
        files=uploaded_files,
        message="Document uploaded successfully!"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
