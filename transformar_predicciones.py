import os
import config
import pandas

path_close = os.path.join(config.path_datos_aprendizaje, "close.csv")
close_values = pandas.read_csv(path_close, index_col="Date")

path_pred = os.path.join(config.path_datos_aprendizaje, "pred.csv")
pred = pandas.read_csv(path_pred, index_col="Date")
idx = pred.index
cols = close_values.columns

# debemos coger el último valor close, y fila a fila y columna a columna, calcular el valor siguiente
previous_row = close_values.tail(1).values.tolist()[0]
list_pred = pred.values.tolist()
new_data = []
for i, row in enumerate(list_pred):
    index = pred.index.tolist()[i]
    new_row = []
    for j, value in enumerate(row):
        col_name = pred.columns.tolist()[j]
        growth = pred.at[index, col_name]
        new = previous_row[j] * (growth + 1)
        new_row.append(new)
    previous_row = new_row
    new_data.append(previous_row)

final = pandas.DataFrame.from_records(new_data, columns=cols)
final["Date"] = idx
final.set_index("Date", inplace=True)

path_final = os.path.join(config.path_datos_aprendizaje, "final_pred.csv")
final.to_csv(path_final, index=True, index_label="Date")
