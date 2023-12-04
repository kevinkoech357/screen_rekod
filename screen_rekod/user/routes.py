from flask import (
    Blueprint,
    render_template,
    send_from_directory,
    request,
    current_app,
    jsonify,
    abort,
    make_response,
)
from flask_login import current_user
from screen_rekod.models.videos import Video
from screen_rekod.models.user import User
from screen_rekod import db
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from mimetypes import guess_extension
import os

# Create the user blueprint
user = Blueprint("user", __name__)

# Specify the allowed file extensions and the upload folder
ALLOWED_EXTENSIONS = {"mp4"}

# Helper function to check if the file has an allowed extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@user.route("/", methods=["GET"])
def index():
    """
    Render the index page.

    Returns:
        str: HTML content for the index page.
    """
    return render_template("index.html")


@user.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """
    Render the user's dashboard with associated videos.

    Returns:
        str: HTML content for the dashboard page.
    """
    try:
        # Getting videos associated with the current_user
        user_videos = Video.query.filter_by(user=current_user).all()

        return render_template("dashboard.html", user_videos=user_videos)
    except Exception as e:
        print(str(e))
        return "Something is wrong!"


@user.route("/videos/<filename>", methods=["GET"])
@login_required
def serve_video(filename):
    """
    Serve a video file.

    Args:
        filename (str): The name of the video file.

    Returns:
        str: Video file content.
    """
    try:
        # Construct the full path to the video file by joining the directory path
        video_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
    except FileNotFoundError:
        return "Video not found", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@user.route("/download/<filename>", methods=["GET"])
@login_required
def download_video(filename):
    """
    Download a video file.

    Args:
        filename (str): The name of the video file.

    Returns:
        str: Video file content as an attachment.
    """
    try:
        # Construct the full path to the video file by joining the directory path
        video_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        return send_from_directory(
            current_app.config["UPLOAD_FOLDER"], filename, as_attachment=True
        )
    except FileNotFoundError:
        return "Video not found", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@user.route("/upload", methods=["POST"])
@login_required
def upload():
    try:
        with current_app.app_context():
            logger = current_app.logger

            # Check if the request has a file in the "video_file" field
            if "video_file" not in request.files:
                return make_response(
                    jsonify({"status": "error", "message": "No video file provided"}),
                    400,
                )

            # Get the file from the request
            video_file: FileStorage = request.files["video_file"]

            # Get other data from the request
            title = request.form.get("title", "")
            description = request.form.get("description", "")
            browser_name = request.form.get("browserName", "")
            browser_version = request.form.get("browserVersion", "")
            browser_layout = request.form.get("browserLayout", "")
            operating_system = request.form.get("operatingSystem", "")

            # Check if the file extension is allowed
            extension = guess_extension(video_file.mimetype)
            if not extension or extension[1:] not in ALLOWED_EXTENSIONS:
                return make_response(
                    jsonify({"status": "error", "message": "Invalid file extension"}),
                    400,
                )

            # Generate a unique filename with consecutive numbering
            i = 1
            while True:
                filename = f"screen_rekod-{i}{extension}"
                dst = os.path.join(
                    current_app.config.get("UPLOAD_FOLDER", "uploads"),
                    secure_filename(filename),
                )
                if not os.path.exists(dst):
                    break
                i += 1

            # Save the file to disk
            video_file.save(dst)

            # Create a new Video record in the database
            new_video = Video(
                title=title,
                description=description,
                filename=filename,
                user=current_user,
                browser_name=browser_name,
                browser_version=browser_version,
                browser_layout=browser_layout,
                operating_system=operating_system,
            )

            db.session.add(new_video)
            db.session.commit()

            # Convert the Video object to a dictionary using the format() method
            video_dict = new_video.format()

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "File successfully uploaded",
                        **video_dict,
                    }
                ),
                201,
            )

    except Exception as e:
        logger.error(f"Error during upload: {str(e)}")
        return make_response(
            jsonify({"status": "error", "message": "Internal server error"}),
            500,
        )
