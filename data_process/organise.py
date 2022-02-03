import os

import pandas as pd


class OrganiseData(object):
    def __init__(self, base_path, name_path):
        self.path = base_path
        self.name_path = name_path

    def get_name_set(self):
        name_set = pd.read_csv(self.name_path, header=None)
        return name_set

    def ohlc(self, name):
        path = self.path + '/{name}.json'.format(name=name)
        if os.path.exists(path):
            dataset = pd.read_json(path)
            return dataset.iloc[:, 0:5]
        print('not find(ohlc)')

    def mkcap(self, name):
        path = self.path + '/{name}.json'.format(name=name)
        if os.path.exists(path):
            dataset = pd.read_json(path)
            return dataset.iloc[:, [0, 5, 6]]

    def get_all_mk(self):
        names = pd.read_csv(self.name_path, header=None)[0]
        token_name = []
        marketcap = []
        for name in names:
            path = self.path + '/{name}.json'.format(name=name)
            if os.path.exists(path):
                latest_marketcap = pd.read_json(path).iloc[0, 6]
                token_name.append(name)
                marketcap.append(latest_marketcap)
        return pd.DataFrame({'name': token_name, 'marketcap': marketcap})

    def get_all_volume(self):
        names = pd.read_csv(self.name_path, header=None)[0]
        token_name = []
        volume = []
        for name in names:
            path = self.path + '/{name}.json'.format(name=name)
            if os.path.exists(path):
                latest_volume = pd.read_json(path).iloc[0, 5]
                token_name.append(name)
                volume.append(latest_volume)
        return pd.DataFrame({'name': token_name, 'volume': volume})

    def get_all_close(self):
        names = pd.read_csv(self.name_path, header=None)[0]
        token_name = []
        close = []
        for name in names:
            path = self.path + '/{name}.json'.format(name=name)
            if os.path.exists(path):
                latest_close = pd.read_json(path).iloc[0, 4]
                token_name.append(name)
                close.append(latest_close)
        return pd.DataFrame({'name': token_name, 'close': close})

    def get_percent(self):
        dataset = self.get_all_mk()
        sum = 0
        for mkc in dataset['marketcap']:
            sum += (mkc / 1000000)
        percent = dataset['marketcap'] / 1000000 / sum
        dataset['percent'] = percent
        return dataset

    def average_earning_rate(self, name):
        data = self.ohlc(name)
        open = data.iloc[:, 1]
        close = data.iloc[:, 4]
        earning_rate = [(close[i] - open[i]) / open[i] for i in range(len(close))]
        average_earning_rate = sum(earning_rate) / len(earning_rate)
        return average_earning_rate

    def average_fluctuation(self, name):
        data = self.ohlc(name)
        high = data.iloc[:, 2]
        low = data.iloc[:, 3]
        diff = [high[i] - low[i] for i in range(len(high))]
        average_diff = sum(diff) / len(diff)
        aver_fluctuation = sum([(diff[i] - average_diff)**2 for i in range(len(diff))]) / len(diff)
        return aver_fluctuation


    def close_modify(self, dataset):
        new_set = []
        for i in range(len(dataset)):
            if i == 0:
                new_set.append(0)
            else:
                new_set.append(dataset[i] - dataset[i-1])
        return new_set




if __name__ == '__main__':
    base_path = '../json_dataset'
    name_path = '../processed_dataset/cleaned_names.csv'
    test = OrganiseData(base_path, name_path)
    data = test.average_earning_rate('decentraland')
    print(data)
