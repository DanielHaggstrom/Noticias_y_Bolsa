import os

import numpy
import pandas
from keras.layers import BatchNormalization, Cropping1D, Dense, LSTM
from keras.models import Sequential
from keras.optimizers import Adam
from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler

import config


def split_sequences(data, n_steps, horizon, target_list):
    targets = numpy.array([data.columns.get_loc(column_name) for column_name in target_list])
    sequences = data.to_numpy()
    x_values, y_values = [], []

    for index in range(len(sequences)):
        end_index = index + n_steps
        if end_index + horizon >= len(sequences):
            break
        x_values.append(sequences[index:end_index, :])
        y_values.append(sequences[end_index : end_index + horizon, targets])

    return numpy.array(x_values), numpy.array(y_values)


def main():
    path = os.path.join(config.path_datos_aprendizaje, "dataset.csv")
    data = pandas.read_csv(path, index_col="Date")

    scaler = MinMaxScaler()
    columns = data.columns
    index = data.index
    scaled_data = scaler.fit_transform(data)
    data = pandas.DataFrame(scaled_data, columns=columns)
    data.set_index(index, inplace=True)

    sep = int(len(data) * 0.8)
    training_data = data.iloc[0:sep]
    testing_data = data.iloc[sep:]

    window = 30
    horizon = 5
    targets = [column_name for column_name in data.columns if "growth" in column_name]

    x_train, y_train = split_sequences(training_data, window, horizon, targets)
    x_test, y_test = split_sequences(testing_data, window, horizon, targets)
    print(x_train.shape)
    print(y_train.shape)

    model = Sequential()
    model.add(BatchNormalization(input_shape=(window, x_train.shape[2])))
    model.add(LSTM(200, return_sequences=True, activation="relu"))
    model.add(BatchNormalization())
    model.add(LSTM(200, return_sequences=True, activation="relu"))
    model.add(BatchNormalization())
    model.add(LSTM(y_train.shape[2], activation="relu", return_sequences=True))
    model.add(BatchNormalization())
    model.add(Cropping1D((x_train.shape[1] - horizon, 0)))
    model.add(BatchNormalization())
    model.add(Dense(len(targets)))
    model.compile(optimizer=Adam(learning_rate=1e-2), loss="mse")
    model.summary()

    history = model.fit(
        x_train,
        y_train,
        epochs=300,
        batch_size=window * 10,
        validation_data=(x_test, y_test),
        verbose=2,
    )

    pyplot.plot(history.history["loss"])
    pyplot.plot(history.history["val_loss"])
    pyplot.title("model train vs validation loss")
    pyplot.ylabel("loss")
    pyplot.xlabel("epoch")
    pyplot.legend(["train", "validation"], loc="upper right")
    pyplot.show()

    prediction_input = x_test[0]
    prediction = model.predict(prediction_input.reshape(1, x_test[0].shape[0], x_test[0].shape[1]))
    print(prediction)


if __name__ == "__main__":
    main()
