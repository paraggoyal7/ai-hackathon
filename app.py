from flask import Flask, request
import os
from flask_cors import CORS
from AssemblyParser import generate_transcript
from agents.sentiment_pipline import run_agent as sentiment_agent
from agents.sop_pipeline import run_agent as sop_agent
import concurrent.futures

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'


@app.route("/upload-file", methods=["POST"])
def upload_file():
    # Get text input from the form
    text_data = request.form.get("text_input")

    # Get the uploaded audio file
    audio_file = request.files.get("audio_file")
    file_name = audio_file.filename
    current_directory = os.path.abspath(os.getcwd())
    if audio_file:
        file_path = os.path.join(current_directory, file_name)
        audio_file.save(file_path)
        return {"path": file_path}


@app.route("/process-file", methods=["POST"])
def process_file():
    json_input = request.get_json()
    audio_path = json_input.get("path")
    transcript_path, transcript = generate_transcript(audio_path)

    sentiment_resp = None
    sop_resp = None

    with concurrent.futures.ProcessPoolExecutor() as executor:
        sentiment_future = executor.submit(sentiment_agent, transcript_path, audio_path)
        sop_future = executor.submit(sop_agent, transcript_path)

        sentiment_resp = sentiment_future.result()
        sop_resp = sop_future.result()

    return {
        "sentiment_resp": sentiment_resp,
        "sop_resp": sop_resp,
        "transcript": transcript
    }


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)