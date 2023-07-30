from flask import Flask, request, render_template, redirect, url_for
import joblib

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
    x = [[url]]
    # Predict target values
    y_pred = model.predict(x)[0]
    # Print prediction
    return render_template('result.html', prediction_text='The URL is {}'.format(y_pred[0]))


if __name__ == '__main__':
    app.run(port=5000, debug=True)