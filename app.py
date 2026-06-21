from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

# Replace with your bucket name
BUCKET_NAME = "employee-document-storage-unique"

# Uses EC2 IAM Role automatically
s3 = boto3.client("s3")

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

        # Upload file directly to S3
        s3.upload_fileobj(
            uploaded_file,
            BUCKET_NAME,
            uploaded_file.filename
        )

        uploaded_files.append({
            "employee": employee_name,
            "filename": uploaded_file.filename
        })

    return render_template(
        "index.html",
        files=uploaded_files,
        message="Document uploaded successfully to S3!"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
