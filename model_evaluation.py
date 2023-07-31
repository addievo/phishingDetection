import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def get_analytics():
    # Load saved model

    model = joblib.load('models/phishing_detection_model.pkl')

    # Load data

    combined_data = pd.read_csv("data/5.urldata.csv")

    # Prepare data
    combined_data = combined_data.drop("Web_Traffic", axis=1)  # drop 'Web_Traffic' first
    x = combined_data.drop(['Domain', 'Label'], axis=1)  # then drop 'Domain' and 'Label'
    y = combined_data['Label']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Predict target values

    y_pred = model.predict(x_test)

    # Calculate Metrics

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Print Metrics

    print("Multilayer Perceptrons: Accuracy: {:.3f}".format(accuracy))
    print("Multilayer Perceptrons: Precision: {:.3f}".format(precision))
    print("Multilayer Perceptrons: Recall: {:.3f}".format(recall))
    print("Multilayer Perceptrons: F1: {:.3f}".format(f1))

    # Calculate AUC-ROC

    auc = roc_auc_score(y_test, y_pred)

    # Print AUC-ROC

    print("Multilayer Perceptrons: AUC-ROC: {:.3f}".format(auc))

    # Generate ROC curve values for fpr, tpr, thresholds

    fpr, tpr, thresholds = roc_curve(y_test, y_pred)


    # Plot ROC curve
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()


if __name__ == "__main__":
    get_analytics()
