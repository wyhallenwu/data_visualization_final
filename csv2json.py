import os
import pandas as pd

name_set = pd.read_csv('./dataset/name.csv')
names = name_set['name']
print(names)
names.to_csv('./name.csv', index=0, header=0)
for name in names:
    filename = './dataset/{name}.csv'.format(name=name)
    if os.path.exists(filename):
        data = pd.read_csv(filename)
        data = data.iloc[:, 1:]
        data.to_json('./json_dataset/{name}.json'.format(name=name), orient='records')
