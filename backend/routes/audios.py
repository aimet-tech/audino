import os

from flask import send_from_directory, jsonify
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_raw_jwt

from backend import app, redis_client

from backend.models import Data


@app.route("/audios/<path:file_name>")
@jwt_required
def send_audio_file(file_name):
    try:
        jti = get_raw_jwt()["jti"]
        entry = redis_client.get(jti)
        if entry is None:
            return jsonify(message="Unauthorized access!"), 401
        return send_from_directory(app.config["UPLOAD_FOLDER"], file_name)
    except Exception as e:
        app.logger.error(e)
        return jsonify(message=f"Error loading the audio\n{str(e)}"), 404
