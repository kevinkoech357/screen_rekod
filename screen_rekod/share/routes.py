from flask import (
    Blueprint,
    jsonify,
    render_template,
    url_for,
    abort,
    current_app,
    send_from_directory,
)
from screen_rekod.models.videos import Video
import os
import logging

share = Blueprint("share", __name__)

logger = logging.getLogger(__name__)


@share.route("/generate_share_link/<string:video_id>", methods=["GET"])
def generate_share_link(video_id):
    """
    Generate a shareable link for a video.

    Args:
        video_id (str): The unique identifier of the video.

    Returns:
        JSON response containing the shareable link.
    """
    try:
        # Retrieve the video from the database based on the provided video_id
        video = Video.query.get(video_id)

        # Check if the video is valid
        if not video:
            logger.warning("Video with ID %s not found", video_id)
            abort(404)

        # Generate the shareable link
        shareable_link = url_for(
            "share.watch_video",
            video_id=video_id,
            sharing_token=video.sharing_token,
            _external=True,
        )
        logger.info("Shareable link generated successfully for Video ID: %s", video_id)
        return jsonify({"shareable_link": shareable_link})

    except Exception as e:
        logger.error("Error generating shareable link: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


@share.route("/watch/<string:video_id>/<string:sharing_token>", methods=["GET"])
def watch_video(video_id, sharing_token):
    """
    Render the video watch page.

    Args:
        video_id (str): The unique identifier of the video.
        sharing_token (str): The sharing token associated with the video.

    Returns:
        Response: Rendered template or an error page.
    """
    try:
        # Retrieve the video from the database based on the provided video_id
        video = Video.query.get(video_id)

        # Check if the video and sharing token are valid
        if video and video.sharing_token == sharing_token:
            # Render a template that displays the video
            video_path = os.path.join(
                current_app.config.get("UPLOAD_FOLDER", "uploads"), video.filename
            )
            # Log the video path for debugging
            logger.info("Video path: %s", video_path)

            logger.info("Successfully rendered video page for Video ID: %s", video_id)

            return render_template("watch_video.html", video=video)

        # If the video or sharing token is not valid, redirect to an error page
        logger.warning("Invalid video or sharing token. Video ID: %s", video_id)
        return render_template("404.html")

    except Exception as e:
        logger.error("Error handling shareable link: %s", str(e))
        return render_template("500.html")


@share.route(
    "/get_video/<string:video_id>/<string:sharing_token>/<string:filename>",
    methods=["GET"],
)
def get_video(video_id, sharing_token, filename):
    """
    Serve a video file for viewing based on the provided video ID, sharing token, and filename.

    Args:
        video_id (str): The unique identifier of the video.
        sharing_token (str): The sharing token associated with the video.
        filename (str): The name of the video file.

    Returns:
        Response: The video file if the provided parameters are valid, or a 404 error page.
    """
    try:
        # Retrieve the video from the database based on the provided video_id
        video = Video.query.get(video_id)

        # Check if the video is valid and the sharing token matches
        if (
            video
            and video.sharing_token == sharing_token
            and video.filename == filename
        ):
            # Construct the path to the video file
            video_directory = current_app.config.get("UPLOAD_FOLDER", "uploads")
            return send_from_directory(video_directory, filename, as_attachment=False)

        # If the video or sharing token is not valid, return a 404 error
        logger.warning(
            "Invalid video, sharing token, or filename. Video ID: %s", video_id
        )
        return render_template("404.html")

    except Exception as e:
        logger.error("Error serving video: %s", str(e))
        return render_template("500.html")
