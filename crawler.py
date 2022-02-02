import os
import pathlib
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains


class CoinMarketCap(object):
    def __init__(self):
        self.url = 'https://coinmarketcap.com/view/metaverse/'
        self.path = 'web_driver/chromedriver'

    def open_driver(self):
        '''Open Chrome driver.

        Returns:
            webdriver
        '''
        option = Options()
        option.add_argument('--user-data-dir=' + r'/home/wuyuheng/.config/google-chrome/')
        # option.add_argument('headless')
        driver = webdriver.Chrome(self.path, options=option)
        return driver

    def get_name(self):
        '''Fetch metaverse tokens' names from coinmarketcap.

        Result will be stored in dataset/name.csv
        '''
        driver = self.open_driver()
        driver.get(self.url)
        name_set = []
        sleep(10)
        for i in range(100):
            if i % 5 == 0:
                sleep(2)
            xpath = '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/table/tbody/tr[{index}]/td[3]/div/a/div/div/p'.format(index = i + 1)
            name = driver.find_element(By.XPATH, xpath).text
            name = name.lower()
            print(name)
            name_set.append(name)
        self.export_name(name_set)

    def export_name(self, data):
        dataframe = pd.DataFrame({'name': data})
        dataframe.to_csv('dataset/name.csv')

    def read_name(self):
        dataset = pd.read_csv('processed_dataset/cleaned_names.csv', header=None)
        return dataset.iloc[:, 0]

    def export_history_data(self):
        '''Collect history data about metaverse tokens.

        It will collect latest 30 days information of names in name.csv. Result will be stored in dataset/
        '''
        BaseUrl = 'https://coinmarketcap.com/currencies/{}/historical-data/'
        name_set = self.read_name()
        for name in name_set:
            if not os.path.exists('./dataset/{name}.csv'.format(name=name)):
                url = BaseUrl.format(name).replace(' ', '-')
                count = 0
                while count < 3:
                    try:
                        self.colloect_one_kind(url, name)
                    except:
                        count = count + 1
                        continue
                    else:
                        break
                if count == 3:
                    print('jump {name}'.format(name=name))
                    continue
                print('success {name}'.format(name=name))

    def scroll_down(self, driver):
        driver.execute_script('window.scrollBy(0,6000)')
        ac = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[2]/div/div[3]/div/div/p[1]/button')
        ActionChains(driver).move_to_element(ac).click(ac).perform()
        sleep(2)


    def colloect_one_kind(self, url, name):
        driver = self.open_driver()
        driver.get(url)
        sleep(5)
        self.scroll_down(driver)
        self.scroll_down(driver)
        self.scroll_down(driver)
        dataset = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'MarketCap'])
        for i in range(120):
            if i % 30 == 0:
                sleep(1)
            xpath = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[3]/div/div/div[2]/table/tbody/tr[{index_}]'.format(index_=i+1)
            dataset = self.row_collect(xpath, driver, dataset)
        dataset.reset_index(inplace=True)
        dataset.set_index('Date')
        dataset.to_csv('./dataset/{path_name}.csv'.format(path_name=name), index=False, header=True)
        print('success')
        driver.quit()

    def row_collect(self, base_xpath, driver, dataset):
        index = 1
        row_data = {'Date': None, 'Open': None, 'High': None, 'Low': None, 'Close': None, 'Volume': None, 'MarketCap': None}
        for key in row_data.keys():
            xpath = base_xpath + '/td[{index_}]'.format(index_=index)
            driver.implicitly_wait(2)
            info = driver.find_element(By.XPATH, xpath)
            info = info.text.replace('$', '').replace(',', '')
            row_data[key] = str(info)
            index = index + 1
        row_data = pd.DataFrame(row_data, index=[0])
        dataset = pd.concat([dataset, row_data])
        return dataset


if __name__ == '__main__':
    test = CoinMarketCap()
    # test.get_name()
    test.export_history_data()
