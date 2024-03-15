import os
import demucs
import demucs.separate
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Use another model and segment:
# separator = demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", "track with space.mp3"])
extensions = ["mp3", "wav", "ogg", "flac"]  # we will look for all those file types.


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route("/upload", methods=['POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        file_to_upload = request.files['file']
    if file_to_upload.filename == '':
        return jsonify({'error': 'No selected file'})

    if file_to_upload and allowed_file(file_to_upload.filename):
        origin, separated = demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", file_to_upload])
        for file, sources in separated:
            for stem, source in sources.items():
                demucs.api.save_audio(source, f"{stem}_{file}", samplerate=separator.samplerate)
        return jsonify({'message': 'File uploaded successfully'})

    return jsonify({'error': 'Invalid file extension'})