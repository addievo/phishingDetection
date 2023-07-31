import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import joblib
from sklearn.ensemble import RandomForestClassifier


def load_data():
    combined_data = pd.read_csv("data/5.urldata.csv")

    # Drop 'Web Traffic' column
    combined_data = combined_data.drop('Web_Traffic', axis=1)

    # Split features and target y

    x = combined_data.drop(['Domain', 'Label'], axis=1)
    y = combined_data['Label']

    return x, y


def split_data(x, y):
    # Split data into train and test sets

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    return x_train, x_test, y_train, y_test


# Creating and saving model
# Increasing number of layers, from 3 to 6, with 100 neurons each.
def main():
    x, y = load_data()
    x_train, x_test, y_train, y_test = split_data(x, y)

    # Fit model to training data

    model = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
    model.fit(x_train, y_train)

    # predicting the target value from model for samples

    y_test_model = model.predict(x_test)
    y_train_model = model.predict(x_train)

    # compute accuracy of model

    accuracy_test = accuracy_score(y_test, y_test_model)
    accuracy_train = accuracy_score(y_train, y_train_model)

    # print accuracy of model

    print("Multilayer Perceptrons: Accuracy on training Data: {:.3f}".format(accuracy_test))
    print("Multilayer Perceptrons: Accuracy on test Data: {:.3f}".format(accuracy_train))

    # Save model

    joblib.dump(model, 'models/phishing_detection_model.pkl')


if __name__ == "__main__":
    main()
