import os
import uuid
from flask import Flask, flash, request, redirect, url_for, send_file, after_this_request, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from yolov5 import detect as testmodel

MODEL = "./models/excavator.pt"
IMG_SIZE = 224

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADER'] = 'Content-Type'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/serve_file/<file>")
@cross_origin()
def serve_file(file):
    file_path = f"./{file}"
    return send_file(file_path)


@app.route("/serve_original/<file>")
@cross_origin()
def serve_original(file):
    file_path = f"uploads/{file}"

    # @after_this_request
    # def remove_file(response):
    #     os.remove(file_path)
    #     return response

    return send_from_directory(file_path)


@app.route("/serve_result/<path:file>")
@cross_origin()
def serve_result(file):
    file_path = f"image_results/{file}"

    # @after_this_request
    # def remove_file(response):
    #     os.remove(file_path)
    #     return response

    print(file_path)
    return send_file(file_path)


@app.route("/upload", methods=['POST'])
@cross_origin()
def upload():
    # check if the post request has the file part
    if 'image' not in request.files or request.files['image'].filename == '':
        return {"error": "No image in request"}
    file = request.files['image']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        file_name = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)

        try:
            testmodel.run(
                weights = MODEL, 
                source = file_path, 
                imgsz = (IMG_SIZE, IMG_SIZE),
                project = 'image_results'
            )

            l = list(filter(lambda x: x.startswith('exp'), os.listdir('./image_results')))
            l.sort()

            if l:
                detection_img = os.path.join(l[-1], os.listdir('image_results/' + l[-1])[0])
            else:
                detection_img = 'Error !'
        
        except Exception as e:
            detection_img = f'failed with error : {e}'

        return {
            "original": f"/serve_original/{file_name}",
            "detection": f"/serve_result/{detection_img}",
        }

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8001)