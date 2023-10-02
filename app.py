from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
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
            "filepath": self.filePath,
            "videoName": self.videoName,
            "Transcript": self.transcript
        }

# Create the "videos" table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def status():
    '''Status of the app'''
    return jsonify({"message": "Up and running"})

@app.route('/start')
def request_recording():
    '''This is the first step
        creates a blank mp4 file in storage
        assigns a name to it which is the current time
        assigns a uuid to it
        returns the uuid to the client for further streaming
        the transcript at this time is None
    '''
    vid_id = str(uuid.uuid4())
    file_name = f'untitled_{datetime.now().strftime("%d_%m_%yT%H_%M_%S")}.mp4'
    file_path = str(video_directory / file_name)
    new_video = Video(id=vid_id, video_name=file_name, file_path=file_path, transcript='')
    session.add(new_video)
    session.commit()

    return jsonify({"Message": "This is the video details", "video": new_video.to_json()})

@app.route('/upload/<vidID>', methods=["POST"])
def start_recording(vid_id):
    '''This is the second part
        Receives chunks of blob data from client
        Writes this data to the file that was created in part one above
        The filepath is gotten by using the videoID sent in the part one above
        Once all data has been written, returns a success message
    '''
    video = session.query(Video).filter_by(id=vid_id).first()
    file_path = video.file_path

    with open(str(file_path), 'ab') as video_file:
        while True:
            chunks = request.stream.read(4096)
            if len(chunks) == 0:
                break
            video_file.write(chunks)
            
    return jsonify({"Message": "Blob data received and saved", "video": video.to_json()}), 200

@app.route('/done_recording/<vidID>')
def stop_recording(vid_id):
    '''This is the third step
        Processes the video already gotten
        The file path is gotten which already contains the blob datas.
        Sub prpcess is used to transcribe it and the transcription is saved
        to video.transcript
    '''
    video = session.query(Video).filter_by(id=vid_id).first()
    video_file = video.file_path

    # Use subprocess to convert the video file to audio
    transcript = subprocess(run_transcription(video_file))
    
    # Error handlers
    if len(transcript) == 0:
        return jsonify("Unable to transcribe video"), 500
    video.transcript = transcript
    # Return the full video
    return jsonify({"Video": video.to_json()})

@app.route('/all')
def all_videos():
    '''Returns the path of all videos'''
    videos = session.query(Video).all()
    vid = [{'videos': video.to_json()} for video in videos]
    return jsonify(vid)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
