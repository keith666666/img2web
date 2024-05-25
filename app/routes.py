# app/routes.py
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app,
    redirect,
    url_for,
    send_file,
)
import os
from .html_generator import generate_html_by_image_file, generate_unique_id
from werkzeug.utils import secure_filename
from .tools import limiter

main = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/tmp/<filename>")
def get_tmp_file(filename):
    file_path = os.path.join("static/tmp", filename)
    return send_file(file_path)


@main.route("/upload-and-generate", methods=["POST"])
@limiter.limit("3/second")
def upload_and_generate():
    if "file" not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files["file"]

    # Get the content type from the file
    content_type = file.content_type

    # Map MIME types to file extensions
    mime_to_ext = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        # Add more mappings as needed
    }

    # Determine the file extension from the content type
    file_extension = mime_to_ext.get(content_type, "jpg")

    # Create a new file name with the determined extension
    new_file_name = f"{generate_unique_id()}.{file_extension}"
    print(f"original file name: {file.filename}, new file name: {new_file_name}")

    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]
    new_file_path = os.path.join(UPLOAD_FOLDER, new_file_name)

    # Save the file with the new file name
    file.save(new_file_path)
    print(
        f"File successfully uploaded, new file path: {new_file_path}, try to generate html file..."
    )

    page_file_name = generate_html_by_image_file(new_file_path)

    print(f"generate_html_by_image_file sucessfully, page file name: {page_file_name}")

    host = "http://127.0.0.1:5000"
    page_url = f"{host}/tmp/{page_file_name}"
    return (
        jsonify(
            {
                "message": "Url generated successfully",
                "pageUrl": page_url,
            }
        ),
        200,
    )


@main.route("/robots.txt")
def static_from_root():
    file_path = os.path.join(current_app.static_folder, request.path[1:])
    return send_file(file_path)
