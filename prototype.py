import pandas
import os
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from statistics import mean
from sklearn.metrics import r2_score
from sklearn.metrics import explained_variance_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor


# AHORA ESTÁ EN MODO REGRESIÓN

# definimos una función útil para más adelante
def make_time_steps(data, h, w, s, targets):
    # nuestro target es todas las columnas que terminan en '-score'
    window_values = range(1, w + 1, s)
    new_data = pandas.DataFrame()
    for name in data.columns:
        for i in window_values:
            new_col_name = '{}-{}'.format(name, i)
            new_data[new_col_name] = data[name].shift(i)
    new_targets = pandas.DataFrame()
    for target in targets:
        new_target = '{}+{}'.format(target, h)
        new_targets[new_target] = data[target].shift(-h)
    new_data.dropna(inplace=True)
    print("Filas restantes: " + str(len(new_data)))
    return new_data, new_targets


# lo primero es cargar los datos y prepar el dataframe
path = os.path.join(os.path.dirname(__file__), "datos", "aprendizaje", "dataset.csv")
data = pandas.read_csv(path)
data.set_index("Date", inplace=True)

# TODO normalizar datos

# separamos en test y training
training_data = data.loc["2012-01-01":"2018-12-31"]
testing_data = data.loc["2019-01-01":"2020-12-31"]

# declaramos los parámetros que vamos a usar
horizon = 1
window = 15
step = 1

# obtenemos las columans target y no_target
targets = []
for col in data.columns:
    if "growth" in col:
        targets.append(col)
no_targets = list(set(data.columns).difference(targets))

# obtenemos los time_steps
data_train_shifted, target = make_time_steps(training_data, horizon, window, step, targets)
data_test_shifted, _ = make_time_steps(testing_data, horizon, window, step, targets)

# volvemos a obtener target y no target para el nuevo dataset, que tiene un formato de nombres un poco diferente
targets = []
for col in data_train_shifted.columns:
    if "growth" in col:
        targets.append(col)
no_targets = list(set(data_train_shifted.columns).difference(targets))

# creamos los conjuntos de entrenamiento y testeo, separados en targets y no targets
x_train = data_train_shifted[no_targets]
y_train = data_train_shifted[targets]
x_test = data_train_shifted[no_targets]
y_test = data_train_shifted[targets]

# entrenamos y validamos el modelo
reg = MLPRegressor(hidden_layer_sizes=(255, 255, 255, 255, 255, 255, 255), max_iter=100000000)
model = reg.fit(preprocessing.scale(x_train), preprocessing.scale(y_train))
r2 = reg.score(reg.predict(preprocessing.scale(x_test)), preprocessing.scale(y_test))
print(r2)

