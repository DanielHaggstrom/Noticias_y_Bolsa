import os
import pandas
import config
import numpy
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler

# definimos una función útil para más adelante
def split_sequences(data, n_steps, target_list):
    # todo añadir soporte para horizontes y pasos diferentes
    # indicamos los números de columnas con datos a predecir
    targets = numpy.array([data.columns.get_loc(c) for c in target_list])
    no_targets = numpy.array([i for i in range(len(data.columns)) if i not in targets])
    # transformamos a un array de numpy
    sequences = data.to_numpy()
    X, y = list(), list()
    # iteramos línea a línea (time_step=1)
    for i in range(len(sequences)):
        # comprobamos si el final se pasa del tamaño del dataset
        end_ix = i + n_steps
        if end_ix >= len(sequences):
            break
        # agrupamos el input y el output
        seq_x = sequences[i:end_ix, ]
        # horizon=1
        seq_y = sequences[end_ix, targets]
        X.append(seq_x)
        y.append(seq_y)
    return numpy.array(X), numpy.array(y)


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
training_data = data.loc["2012-01-01":"2018-12-31"]
testing_data = data.loc["2019-01-01":"2020-12-31"]

# declaramos los parámetros que vamos a usar
window = 20

# obtenemos las columans target y no_target
targets = []
for col in data.columns:
    if "growth" in col:
        targets.append(col)
no_targets = list(set(data.columns).difference(targets))

# obtenemos los time_steps
x_train, y_train = split_sequences(training_data, window, targets)
x_test, y_test = split_sequences(testing_data, window, targets)

# entrenamos y validamos el modelo
model = Sequential()
model.add(LSTM(20, input_shape=(window, x_train.shape[2], )))
model.add(Dense(len(targets)))
model.add(Dense(len(targets)))
model.summary()
model.compile(optimizer="adam", loss="mse")
history = model.fit(x_train, y_train, epochs=200, batch_size=window, validation_data=(x_test, y_test), shuffle=False)
model.summary()
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('model train vs validation loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'validation'], loc='upper right')
pyplot.show()
