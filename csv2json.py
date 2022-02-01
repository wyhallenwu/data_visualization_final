import os
import pandas as pd

name_set = pd.read_csv('./dataset/name.csv')
names = name_set['name']
for name in names:
    filename = './dataset/{name}.csv'.format(name=name)
    if os.path.exists(filename):
        data = pd.read_csv(filename)
        data = data.iloc[:, 1:]
        print(data)
        data.to_json('./json_dataset/{name}.json'.format(name=name), orient='records')
