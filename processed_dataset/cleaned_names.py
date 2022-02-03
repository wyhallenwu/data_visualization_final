import pandas as pd
import os

names = pd.read_csv('./cleaned_names.csv', header=None)
new_set = []
for name in names.iloc[:, 0]:
    if os.path.exists('../json_dataset/{name}.json'.format(name=name)):
        new_set.append(name)
names = pd.DataFrame(new_set)
names.to_csv('./cleaned_names.csv', index=False, header=0)
print("end")
