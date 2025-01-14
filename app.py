from flask import Flask
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from keras.models import load_model
from tensorflow.compat.v1.keras.backend import set_session
from skimage.transform import resize
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np


app = Flask(__name__)
print("Loading model")
global sess
sess = tf.compat.v1.Session()
set_session(sess)
global graph
graph = tf.compat.v1.get_default_graph()
with graph.as_default():
    global model
    model = load_model('my_cifar10_model.h5')

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')


@app.route('/prediction/<filename>')
def prediction(filename):
    # Step 1
    my_image = plt.imread(os.path.join('static/uploads', filename))
    # Step 2
    my_image_re = resize(my_image, (32, 32, 3))

    # Step 3
    with graph.as_default():
        set_session(sess)
        probabilities = model.predict(np.array([my_image_re, ]))[0, :]
        print(probabilities)
        # Step 4
        number_to_class = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        index = np.argsort(probabilities)
        predictions = {
            "class1": number_to_class[index[9]],
            "class2": number_to_class[index[8]],
            "class3": number_to_class[index[7]],
            "prob1": probabilities[index[9]],
            "prob2": probabilities[index[8]],
            "prob3": probabilities[index[7]],
        }
    # Step 5
    return render_template('predict.html', predictions=predictions,uploaded_file=filename)

if __name__ == "__main__":
    app.run(debug=True)

