import os
import logging
import traceback
from flask import Flask, render_template, request
import time
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from utils import get_predictions

__author__ = 'hanvitha'

app = Flask(__name__)
app.static_folder = 'static'
# Set the secret key to some random bytes. Keep this really secret! :P
app.secret_key = b'_Blah"gd5HK\n\xec]/'
app.logger.setLevel(logging.DEBUG)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

APP_ROOT = os.getenv('APP_ROOT')
# APP_ROOT = os.getcwd()
test_dir = os.path.join(APP_ROOT, 'testimages')
DEFAULT_HOST = "bcd:8080"
# DEFAULT_HOST = "bcd-demo.apps.cluster-plano-6aa8.plano-6aa8.example.opentlc.com"
DEFAULT_BASE_URL = ("http://%s/" % DEFAULT_HOST) + r"%s"


@app.route("/")
def index(error=None):
    try:
        return render_template("index.html", error=error)
    except Exception as e:
        traceback.print_exc()
        return "Oops..something went wrong! Try again later"

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        img = request.files.get('file')
        if not img:
            return 'Please select an image to predict!!'
        # Here we are just processing single file for time being. We can add more based on the need in future if we want to increase the scope of this app!

        time_stamp = time.strftime("%Y%m%d%H%M%S")
        test_file_path = os.path.join(test_dir, "test_" + time_stamp + ".png")
        img.save(test_file_path)

        # print(time_stamp)
        # print(img_paths)
        if request.method == 'POST':
            prediction = get_predictions(DEFAULT_BASE_URL, test_file_path)[0]
            print("Predictions " + str(prediction))
            if(prediction == 1):
                # print("sending Malign")
                return "Prediction: Malign"
            else:
                # print("sending Benign")
                return "Prediction: Benign"
    except Exception as e:
        traceback.print_exc()
        return "Oops something went wrong! Please try again!!"


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(debug=True)
