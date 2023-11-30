from flask import Blueprint, jsonify, render_template, abort, current_app, request
from flask_login import current_user, login_required
from screen_rekod import db
from screen_rekod.models.videos import Video
import os

# Create video Blueprint
video = Blueprint("video", __name__)


@video.route("/video/<string:video_id>", methods=["GET"])
@login_required
def video_detail(video_id):
    """
    Render the detailed view page for a specific video.

    Args:
        video_id (str): The ID of the video.

    Returns:
        str: HTML content for the video detail page.
    """
    video = Video.query.get(video_id)

    if not video:
        abort(404)

    return render_template("video.html", video=video)


@video.route("/update-video/<string:video_id>", methods=["POST"])
@login_required
def update_video(video_id):
    """
    Update the details of a specific video.

    Args:
        video_id (str): The ID of the video.

    Returns:
        JSON: Response indicating success or error.
    """
    try:
        video = Video.query.get(video_id)

        if not video:
            abort(404)

        # Fetch updated details from the form data
        updated_title = request.form.get("title")
        updated_description = request.form.get("description")

        # Update the video details in the database
        video.title = updated_title
        video.description = updated_description

        # Commit the changes
        db.session.commit()

        return (
            jsonify(
                {"status": "success", "message": "Video details updated successfully"}
            ),
            200,
        )

    except Exception as e:
        # Handle any unexpected errors
        print(str(e))
        return jsonify({"error": str(e)}), 500


@video.route("/delete-video/<string:video_id>", methods=["DELETE"])
@login_required
def delete_video(video_id):
    """
    Delete a specific video.

    Args:
        video_id (str): The ID of the video.

    Returns:
        JSON: Response indicating success or error.
    """
    try:
        video = Video.query.get(video_id)

        if not video:
            abort(404)

        # Delete the video from the database
        db.session.delete(video)
        db.session.commit()

        # Remove the video file from the server storage
        video_path = os.path.join(current_app.config["UPLOAD_FOLDER"], video.filename)
        if os.path.exists(video_path):
            os.remove(video_path)

        return (
            jsonify({"status": "success", "message": "Video deleted successfully"}),
            200,
        )

    except Exception as e:
        # Handle any unexpected errors
        print(str(e))
        return jsonify({"error": str(e)}), 500
