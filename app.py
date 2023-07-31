import joblib
import numpy as np
from flask import Flask, request, render_template

from featureExtraction import featureExtraction

app = Flask(__name__)

# Load saved model
model = joblib.load('models/phishing_detection_model.pkl')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Get the input from post request
    url = request.form['url']
    # Prepare data
    x = featureExtraction(url)

    # Prepare data for model

    x = np.array(x).reshape(1, -1)

    # Predict target values
    y_pred = model.predict(x)

    # Convert prediction to label

    prediction = 'Legitimate' if y_pred[0] == 0 else 'Phishing'

    # Print prediction

    return render_template('result.html', prediction_text='The URL is {}'.format(prediction), url=url, features=x)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
