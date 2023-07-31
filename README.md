# Phishing Detection System

## Table of Contents

- [Project Description](#project-description)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Model Selection and Evaluation](#model-selection-and-evaluation)
- [About the Author](#about-the-author)
- [License](#license)

## Project Description

The Phishing Detection System is a web application that uses machine learning to predict whether a given URL is a phishing site. The application is built using Flask for the backend, with HTML5 and CSS for the frontend.

## Project Structure

The project is structured as follows:

- `static/`: This directory contains static files like CSS and JavaScript.
- `templates/`: This directory contains the HTML templates.
- `models/`: This directory contains the trained model.
- `app.py`: This is the main script that runs the application.
- `featureExtraction.py`: This script contains the feature extraction logic.

## Dependencies

This application requires the following Python libraries, which can be installed by navigating to the project directory and running `pip install -r requirements.txt`:

- Flask
- joblib
- numpy
- python-whois
- scikit-learn

## Usage

You can run the application by executing the `app.py` script:

```bash
python app.py
```
This will start a local server and serve the Phishing Detection System on localhost:5000.

## Model Selection and Evaluation

We initially tried using a Multilayer Perceptron (MLP) for this task, but it did not yield satisfactory results. We then switched to a RandomForest model, which significantly improved the performance of our phishing detection.

![Model Evaluation Image](/static/myplot.png)

## About the Author

Aditya Varma is a computer science graduate from the University of Wollongong. He has a keen interest in AI, cybersecurity, systems analysis, and web development.

## License

This project is licensed under the MIT License - see the LICENSE file for details.