from flask import Blueprint, jsonify, render_template, url_for, abort
from screen_rekod.models.videos import Video

share = Blueprint("share", __name__)


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
            abort(404)

        # Generate the shareable link
        shareable_link = url_for(
            "share.watch_video",
            video_id=video_id,
            sharing_token=video.sharing_token,
            _external=True,
        )
        return jsonify({"shareable_link": shareable_link})

    except Exception as e:
        print(f"Error generating shareable link: {e}")
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
            return render_template("watch_video.html", video=video)

        # If the video or sharing token is not valid, redirect to an error page
        return render_template("404.html")

    except Exception as e:
        print(f"Error handling shareable link: {e}")
        return render_template("500.html")
