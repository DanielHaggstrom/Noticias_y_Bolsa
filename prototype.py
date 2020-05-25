import os
import pandas
import config
import numpy
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import LSTM, Dropout, BatchNormalization
from keras.layers import Dense
from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler


# definimos una función útil para más adelante
def split_sequences(data, n_steps):
    # vamos a realizar una predicción para el siguiente valor de todas las columnas
    # transformamos a un array de numpy
    sequences = data.to_numpy()
    x, y = list(), list()
    # iteramos línea a línea (time_step=1)
    for i in range(len(sequences)):
        # comprobamos si el final se pasa del tamaño del dataset
        end_ix = i + n_steps
        if end_ix >= len(sequences):
            break
        # agrupamos el input y el output
        seq_x = sequences[i:end_ix, ]
        seq_y = sequences[end_ix, ]  # horizon=1 -> end_ix -1 + horizon
        x.append(seq_x)
        y.append(seq_y)
    return numpy.array(x), numpy.array(y)


# lo primero es cargar los datos y prepar el dataframe
path = os.path.join(config.path_datos_aprendizaje, "dataset.csv")
data = pandas.read_csv(path, index_col="Date")

# normalizamos los datos
scaler = MinMaxScaler()
cols = data.columns
indx = data.index
scaled_data = scaler.fit_transform(data)
data = pandas.DataFrame(scaled_data, columns=cols)
data.set_index(indx, inplace=True)

# separamos en test y training
sep = int(len(data) * 0.8)
training_data = data.iloc[0:sep]
testing_data = data.iloc[sep:]

# declaramos los parámetros que vamos a usar
window = 24

# obtenemos los time_steps
x_train, y_train = split_sequences(training_data, window)
x_test, y_test = split_sequences(testing_data, window)

# entrenamos y validamos el modelo
model = Sequential()
model.add(BatchNormalization(input_shape=(window, x_train.shape[2], )))
model.add(LSTM(1000, return_sequences=True, activation="relu"))
model.add(BatchNormalization())
model.add(LSTM(1000, return_sequences=True, activation="relu"))
model.add(BatchNormalization())
model.add(LSTM(1000, return_sequences=True, activation="relu"))
model.add(BatchNormalization())
model.add(LSTM(1000, activation="relu"))
model.add(BatchNormalization())
model.add(Dense(x_train.shape[2]))
model.compile(optimizer=Adam(lr=1e-2), loss="mse")
model.summary()
history = model.fit(x_train, y_train, epochs=200, batch_size=window*10, validation_data=(x_test, y_test), verbose= 2)
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('model train vs validation loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'validation'], loc='upper right')
pyplot.show()

# evaluación contínua
horizon = 10 #va a dar 5 predicciones

# creamos la primera predicción
data1 = x_test[0]
pred = model.predict(data1.reshape(1, x_test[0].shape[0], x_test[0].shape[1]))
data1 = numpy.delete(data1, 0, 0)
data1 = numpy.vstack((data1, pred))

# añadimos nuevas predicciones
for i in range(horizon):
    #input(data)
    pred = model.predict(data1.reshape(1, x_test[0].shape[0], x_test[0].shape[1]))
    data1 = numpy.delete(data1, 0, 0)
    data1 = numpy.vstack((data1, pred))
data1 = scaler.inverse_transform(data1)
print(data1)
