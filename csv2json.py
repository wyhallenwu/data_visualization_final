import os
import pandas as pd

name_set = pd.read_csv('./processed_dataset/cleaned_names.csv', header=None)
names = name_set.iloc[:, 0]
for name in names:
    filename = './dataset/{name}.csv'.format(name=name)
    if os.path.exists(filename):
        print(name)
        data = pd.read_csv(filename)
        data = data.iloc[:, 1:]
        data.to_json('./json_dataset/{name}.json'.format(name=name), orient='records')
