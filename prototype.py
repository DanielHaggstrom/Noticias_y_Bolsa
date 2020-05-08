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
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.multioutput import MultiOutputRegressor


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
    new_targets.dropna(inplace=True)
    new_targets.drop(new_targets.head(len(window_values)).index, inplace=True)
    new_data.drop(new_data.tail(1).index, inplace=True)
    print("Filas restantes: " + str(len(new_data)))
    return new_data, new_targets


# lo primero es cargar los datos y prepar el dataframe
path = os.path.join(os.path.dirname(__file__), "datos", "aprendizaje", "dataset.csv")
data = pandas.read_csv(path)
data.set_index("Date", inplace=True)

# normalizamos los datos
data = (data-data.mean())/data.std()
print(data)

# separamos en test y training
training_data = data.loc["2012-01-01":"2018-12-31"]
testing_data = data.loc["2019-01-01":"2020-12-31"]

# declaramos los parámetros que vamos a usar
horizon = 1
window = 20
step = 1

# obtenemos las columans target y no_target
targets = []
for col in data.columns:
    if "growth" in col:
        targets.append(col)
no_targets = list(set(data.columns).difference(targets))

# obtenemos los time_steps
x_train, y_train = make_time_steps(training_data, horizon, window, step, targets)
x_test, y_test = make_time_steps(testing_data, horizon, window, step, targets)

# entrenamos y validamos el modelo
reg = MLPRegressor(hidden_layer_sizes=(800, 800), max_iter=100000000)
reg.fit(x_train, y_train)
r2 = reg.score(x_test, y_test)
print("MLP")
print(mean_squared_error(reg.predict(x_test), y_test))

"""
svr = MultiOutputRegressor(SVR())
svr.fit(x_train, y_train)
r2 = svr.score(x_test, y_test)
print("SVR")
print(mean_squared_error(x_test, y_test))"""
