import json
import pandas as pd


# read data
class DataProcess:
    """Fetch and prepare data for further using.

    The data will be UTF-8 encoded.

    Args:
        filename: A string format filename.
    """
    def __init__(self, filename):
        self.filename = filename

    def fetch_data(self):
        with open(self.filename, 'r', encoding='utf8') as f:
            dataset = json.load(f)
        # data clean
        for i in range(len(dataset['weibo'])):
            dataset['weibo'][i]['content'] = dataset['weibo'][i]['content'].replace('#亲爱的树洞#', '')
        data = pd.DataFrame(dataset['weibo'])
        return data


if __name__ == '__main__':
    # test = DataProcess('dataset/dataset2019.json')
    # dataset = test.fetch_data()
    pass
