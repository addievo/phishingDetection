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

    # Compute feature names that are set to 1
    feature_names = ['having_IP_Address', 'having_At_Symbol', 'URL_Length', 'URL_Depth',
                     'Redirection', 'https_In_Url', 'URL_Short', 'Prefix/Suffix', 'DNS_Record',
                     'Domain_Age', 'Domain_Expiry', 'iFrame', 'Mouse_Over', 'Right_Click', 'Forwarding']

    # Only compute suspicious features if the prediction is 'Phishing'
    suspicious_features = []
    if prediction == 'Phishing':
        suspicious_features = [feature for feature, value in zip(feature_names, x[0]) if value == 1]
    # Print prediction

    return render_template('result.html', prediction_text='{}'.format(prediction), url=url, features=suspicious_features)


if __name__ == '__main__':
    app.run(port=5202, debug=True)
