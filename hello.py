import os
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


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

        return jsonify({'message': 'File uploaded successfully'})

    return jsonify({'error': 'Invalid file extension'})