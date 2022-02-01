import pandas as pd
import os


names = pd.read_csv('./processed_dataset/cleaned_names.csv', header=None)
names_list = []
marketcap_close = []
close_list = []
for name in names.iloc[:, 0]:
    names_list.append(name)
    path = './json_dataset/{name}.json'.format(name=name)
    if os.path.exists(path):
        dataset = pd.read_json(path)
        marketcap_close.append(dataset.iloc[0, 6])
        close_list.append(dataset.iloc[0, 4])

marketcap_close = {'name': names_list, 'close': close_list, 'MarKetCap': marketcap_close}
data = pd.DataFrame(marketcap_close)
print(data)
data.to_csv('./processed_dataset/marketcap_close.csv', index=False)
