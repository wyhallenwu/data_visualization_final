import pandas as pd
import os

names = pd.read_csv('../processed_dataset/cleaned_names.csv', header=None)
names_list = []
marketcap_list = []
for name in names.iloc[:, 0]:
    names_list.append(name)
    path = '../json_dataset/{name}.json'.format(name=name)
    if os.path.exists(path):
        dataset = pd.read_json(path)
        marketcap_list.append(dataset.iloc[0, 6])

marketcap_dict = {'name': names_list, 'MarKetCap':marketcap_list}
marketcap = pd.DataFrame(marketcap_dict)
marketcap.to_csv('./marketcap.csv', index=False)