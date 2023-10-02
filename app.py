from flask import Flask, jsonify, request, send_file
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
import os
import uuid
from flask_cors import CORS
from transcribe_openAI import run_transcription
from datetime import datetime
import subprocess

# Change the videos directory name to "HelpMeOutvideos"
video_directory = Path.cwd() / 'HelpMeOutvideos'

# Create the directory if it doesn't exist
if not video_directory.is_dir():
    os.makedirs(video_directory)

# Create a Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for all origins
CORS(app, resources={r"/*": {"origins": "*"}})

# Create an SQLite database engine
engine = create_engine('sqlite:///videos.db')

# Define the base model for SQLAlchemy
Base = declarative_base()

# Define the Video model
class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(String, primary_key=True)
    filePath = Column(String)
    videoName = Column(String)
    transcript = Column(String, default=None)

    def to_json(self):
        return {
            "id": self.id,
            "videoName": self.videoName,
            "transcript": self.transcript
        }

# Create the "videos" table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def status():
    '''Status'''
    return jsonify({"message": "HelpMeOut Chrome Extension Up"})

'''Create a New Screen Recording'''
@app.route('/api/recording', methods=["POST"])
def request_recording():
    vid_id = str(uuid.uuid4())
    file_name = f'untitled_{datetime.now().strftime("%d_%m_%yT%H_%M_%S")}.mp4'
    file_path = str(video_directory / file_name)
    new_video = Video(id=vid_id, videoName=file_name, filePath=file_path, transcript='')
    session.add(new_video)
    session.commit()

    return jsonify({"recording_id": vid_id}), 201

'''Add Video Chunk to a Recording'''
@app.route('/api/recording/<vid_id>', methods=["POST"])
def start_recording(vid_id):
    video = session.query(Video).filter_by(id=vid_id).first()
    file_path = video.filePath

    with open(str(file_path), 'ab') as video_file:
        while True:
            chunks = request.stream.read(4096)
            if len(chunks) == 0:
                break
            video_file.write(chunks)
            
    return jsonify({"message": "Video chunk added successfully"}), 201


'''Get Video of a Recording'''
@app.route('/api/recording/<vid_id>', methods=["GET"])
def get_recording(vid_id):
    video = session.query(Video).filter_by(id=vid_id).first()
    if not video:
        return jsonify({"error": "Recording not found"}), 404

    return send_file(video.filePath, as_attachment=True)

'''Get All Recordings of a User'''
@app.route('/api/recording/user/<user_id>', methods=["GET"])
def get_user_recordings(user_id):
    videos = session.query(Video).filter_by(user_id=user_id).all()
    recordings = [{'title': video.videoName, 'id': video.id, 'user_id': user_id, 'time': datetime.now().isoformat()} for video in videos]
    return jsonify(recordings), 200

'''Get All Recordings'''
@app.route('/api/recording', methods=["GET"])
def get_all_recordings():
    videos = session.query(Video).all()
    recordings = [{'title': video.videoName, 'id': video.id, 'user_id': '', 'time': datetime.now().isoformat()} for video in videos]
    return jsonify(recordings), 200

'''Update Recording Title'''
@app.route('/api/recording/<vid_id>', methods=["PUT"])
def update_recording_title(vid_id):
    video = session.query(Video).filter_by(id=vid_id).first()
    if not video:
        return jsonify({"error": "Recording not found"}), 404

    data = request.json
    new_title = data.get("title", "")
    video.videoName = new_title
    session.commit()
    return jsonify({"message": "Recording title updated successfully"}), 200

'''Delete a Recording'''
@app.route('/api/recording/<vid_id>', methods=["DELETE"])
def delete_recording(vid_id):
    video = session.query(Video).filter_by(id=vid_id).first()
    if not video:
        return jsonify({"error": "Recording not found"}), 404

    session.delete(video)
    session.commit()
    return jsonify({"message": "Recording deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
