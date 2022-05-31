import os
import uuid
from flask import Flask, flash, request, redirect, url_for, send_file, after_this_request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import testmodel

MODEL = "./models/mobileNet97.h5"
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

    return send_file(file_path)


@app.route("/serve_result/<file>")
@cross_origin()
def serve_result(file):
    file_path = f"image_results/{file}"

    # @after_this_request
    # def remove_file(response):
    #     os.remove(file_path)
    #     return response

    return send_file(file_path)


@app.route("/upload", methods=['POST'])
@cross_origin()
def upload():
    # check if the post request has the file part
    print('image' not in request.files)
    print(request.files['image'].filename == '')
    
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
            predicted_img, predicted_text = testmodel.run_predict(MODEL, file_path, IMG_SIZE)
        except Exception as e:
            predicted_img = f'failed with error : {e}'
            predicted_text = f'failed with error : {e}'
        
        try:
            grad_img = testmodel.run_explain(MODEL, file_path, IMG_SIZE)
        except Exception as e:
            grad_img = f'failed with error : {e}'

        return {
            "original": f"/serve_original/{file_name}",
            "prediction": f"/serve_result/{predicted_img}",
            "gradcam": f"/serve_result/{grad_img}",
            "message": predicted_text
        }

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8001)
