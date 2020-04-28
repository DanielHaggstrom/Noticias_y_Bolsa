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

# AHORA ESTÁ EN MODO CLASSIFICATION


# definimos una función útil para más adelante
def make_time_steps(data, h, w, s, target="Growth"):
    window_values = range(1, w + 1, s)
    new_data = pandas.DataFrame()
    for name in data.columns:
        for i in window_values:
            new_col_name = '{}-{}'.format(name, i)
            new_data[new_col_name] = data[name].shift(i)
    new_target = '{}+{}'.format(target, h)
    new_data[new_target] = data[target].shift(-h)
    return new_data.dropna(), new_target


# preparamos unas variables para guardar los resultados
accuracy = []

# lo primero es cargar los datos y prepar el dataframe
path = "D:\\Coding\\PyCharm Workspace\\ProyectoBigData\\datos\\Prototipo 2\\datos_aprendizaje"
for file in os.listdir(path):
    data = pandas.read_csv(path + "\\" + file)
    data.set_index("Date", inplace=True)
    # separamos en test y training
    training_data = data.loc["2010-01-01":"2019-12-31"]
    testing_data = data.loc["2020-01-01":"2020-12-31"]
    # declaramos los parámetros que vamos a usar
    horizon = 2
    window = 5
    step = 1
    data_train_shifted, target = make_time_steps(data=training_data, h=horizon, w=window, s=step)
    data_test_shifted, _ = make_time_steps(data=testing_data, h=horizon, w=window, s=step)
    x_train, y_train, x_test, y_test = data_train_shifted.iloc[:, :-1], \
                                       data_train_shifted.iloc[:, -1], \
                                       data_test_shifted.iloc[:, :-1], \
                                       data_test_shifted.iloc[:, -1],
    """
    model = SVR(gamma='auto')
    model.fit(x_train, y_train)
    y_svr_pred = model.predict(x_test)
    print(explained_variance_score(y_test, y_svr_pred))
    
    rf = RandomForestRegressor(n_estimators=1000)
    rf.fit(x_train, y_train)
    y_rf_pred = rf.predict(x_test)
    r2.append(explained_variance_score(y_test, y_rf_pred))
    """
    rf = RandomForestClassifier()
    rf.fit(x_train, y_train)
    accuracy.append(accuracy_score(y_test, rf.predict(x_test)))

plt.hist(accuracy)
plt.show()
