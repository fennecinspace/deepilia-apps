import sys
import os
import cv2
import uuid
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image
from keras.models import Model, load_model
from keras.applications.vgg16 import VGG16, preprocess_input #224*224
from keras.applications.xception import Xception, preprocess_input, decode_predictions #299*299
from keras.applications.mobilenet import MobileNet
from PIL import Image, ImageEnhance

#### EXPLAIN ####
import tf_explain
from tf_explain.core.grad_cam import GradCAM
from keras.models import load_model
#################

print("Tensorflow version: " + tf.__version__)
print("Keras version: " + tf.keras.__version__)

def read_classes():
    classes_path = "classes.txt"
    # Récupérer les noms des classes
    with open(classes_path, 'r') as f:
        classes = f.readlines()
        classes = list(map(lambda x: x.strip(), classes))
    num_classes = len(classes)
    return num_classes, classes


def run_predict(model = "models/mobileNet97.h5", image_path = "uploads/fire.jpg", image_size = 224):
    num_classes, classes = read_classes()

    if type(model) is str: # don't load model if it's already preloaded
        model = load_model(model)

    img = cv2.imread(image_path)
    img = cv2.resize(img, (image_size, image_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    x = np.expand_dims(img, axis = 0)

    # predict
    pred = model.predict(x, batch_size = 1)[0]
    prob = pred[np.argmax(pred)]
    class_name = classes[np.argmax(pred)]

    font = cv2.FONT_HERSHEY_COMPLEX 
    textsize = cv2.getTextSize(class_name, font, 1, 2)[0]

    textX = (img.shape[1] - textsize[0]) / 2
    textY = (img.shape[0] + textsize[1]) / 2

    cv2.putText(img, class_name, (int(textX)-10, int(textY)), font, 2, (255,0,0), 6, cv2.LINE_AA)

    img_file_name = str(uuid.uuid4()) + image_path[-4:]
    cv2.imwrite('image_results/' + img_file_name, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    message =  f"Class Name : { class_name } --- Class Probability: {prob * 100:.2f}%"
    print(message)

    return img_file_name, message


def run_explain(model = "models/mobileNet97.h5", image_path = "uploads/fire.jpg", image_size = 224):
    if type(model) is str: # don't load model if it's already preloaded
        model = load_model(model)

    # Load a sample image (or multiple ones)
    img = tf.keras.preprocessing.image.load_img(image_path, target_size = (image_size, image_size))
    img = tf.keras.preprocessing.image.img_to_array(img)
    data = ([img], None)
    
    grad_file_name = str(uuid.uuid4()) + '.png'

    # Start explainer
    explainer = GradCAM()
    grid = explainer.explain(data, model, class_index = 0)  # 281 is the tabby cat index in ImageNet
    explainer.save(grid, ".", 'image_results/' + grad_file_name)

    return grad_file_name