# este script busca probar varias configuraciones para el modelo de regresión
import os
import config
import pandas
import numpy
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler


# definimos la función para dar el formato adecuado a los datos
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
        seq_y = sequences[end_ix, targets]  # horizon=1 -> end_ix -1 + horizon
        X.append(seq_x)
        y.append(seq_y)
    return numpy.array(X), numpy.array(y)


# lo primero es cargar los datos y prepar el dataframe
path = os.path.join(os.path.dirname(__file__), "datos", "aprendizaje", "dataset.csv")
data = pandas.read_csv(path, index_col="Date")

# normalizamos los datos
scaler = MinMaxScaler()
cols = data.columns
indx = data.index
scaled_data = scaler.fit_transform(data)
data = pandas.DataFrame(scaled_data, columns=cols)  # sklearn destruye el índice y nombres de columnas, los recuperamos
data.set_index(indx, inplace=True)

# separamos en test y training
training_data = data.loc["2012-01-01":"2018-12-31"]
testing_data = data.loc["2019-01-01":"2020-12-31"]


# esta función entrena el modelo y genera un gráfico de pérdida, que será útil para la validación
def train_and_validate(window, lstm, layer_num, epoch, path):
    model = Sequential()
    model.add(LSTM(lstm, input_shape=(window, x_train.shape[2])))
    for i in range(layer_num):
        model.add(Dense(len(targets)))
    model.compile(optimizer="adam", loss="mse")
    history = model.fit(x_train, y_train, epochs=epoch, batch_size=window, validation_data=(x_test, y_test),
                        shuffle=False)
    pyplot.plot(history.history["loss"])
    pyplot.plot(history.history["val_loss"])
    pyplot.title("Ventana " + str(window) + " lstm " + str(lstm) + " capas " + str(layer_num))
    pyplot.ylabel("Pérdida (mse)")
    pyplot.xlabel("Epoch")
    pyplot.legend(["Entrenamiento", "Validación"], loc="upper right")
    pyplot.savefig(path)
    pyplot.close()
    return None


targets = []
for col in data.columns:
    if "growth" in col:
        targets.append(col)
no_targets = list(set(data.columns).difference(targets))

# entrenamos y validamos el modelo, iterando sobre los demás parámetros
for lstm in range(1, 1000, 100):
    for layer_num in range(1, 100):
        for window in range(2, 60, 6):
            # comprobamos si esta comprobación ya existe
            path = os.path.join(config.path_graph, "window " + str(window) + " lstm " + str(lstm) + " layer "
                                + str(layer_num) + ".png")
            if os.path.exists(path):
                continue
            # obtenemos los time_steps
            x_train, y_train = split_sequences(training_data, window, targets)
            x_test, y_test = split_sequences(testing_data, window, targets)
            train_and_validate(window, lstm, layer_num, 200, path)
