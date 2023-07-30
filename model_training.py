import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense


def load_data():
    phishing_data = pd.read_csv("data/4.phishing.csv")
    legitimate_date = pd.read_csv("data/3.legitimate.csv")

    # Combine phishing and legitimate data
    combined_data = pd.concat([phishing_data, legitimate_date])


    print(phishing_data['Label'].value_counts())

    # Split features and target y

    x = combined_data.drop(['Domain', 'Label'], axis=1)
    y = combined_data['Label']

    return x, y


def split_data(x, y):
    # Split data into train and test sets

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    return x_train, x_test, y_train, y_test


def normalize_data(x_train, x_test):
    # Normalize data

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    return x_train_scaled, x_test_scaled


def create_model(input_dim):
    # Create model
    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    # Simple model with 32 layers of neurons.
    # Activation function is the Rectified Linear Unit (ReLU)
    # The output layer has one neuron with a sigmoid function to output a value between 0 and 1


    #compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Loss function is binary cross entropy
    # Optimizer is Adam
    # Metrics is accuracy

    return model

def main():
    x, y = load_data()
    x_train, x_test, y_train, y_test = split_data(x, y)
    x_train_scaled, x_test_scaled = normalize_data(x_train, x_test)

    model = create_model(x_train_scaled.shape[1])

    #Fit model to training data

    model.fit(x_train_scaled, y_train, epochs=10, batch_size=32, validation_data=(x_test_scaled, y_test))
    # Epochs is the number of times the model will cycle through the data
    # Batch size is the number of samples per gradient update
    # Validation data is the data on which to evaluate the loss and any model metrics at the end of each epoch

    #Save model

    model.save('models/phishing_detection_model.h5')

if __name__ == "__main__":
    main()
