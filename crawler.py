from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

class CoinMarketCap(object):
    def __init__(self):
        self.url = 'https://coinmarketcap.com/view/metaverse/'
        self.path = 'web_driver/chromedriver'

    def open_driver(self):
        option = Options()
        option.add_argument('--user-data-dir=' + r'/home/wuyuheng/.config/google-chrome/')
        driver = webdriver.Chrome(self.path, options=option)
        return driver

    def download(self):
        driver = self.open_driver()
        driver.get(self.url)
        name_set = []
        for i in range(10):
            if i % 5 == 0:
                sleep(2)
            xpath = '//*[@id="__next"]/div/div[1]/div[2]/div/div/div[2]/table/tbody/tr[{index}]/td[3]/div/a/div/div/p'.format(index = i + 1)
            print(xpath)
            name = driver.find_element(By.XPATH, xpath).text
            name = name.lower()
            name_set.append(name)
        print(name_set)
        self.export_name(name_set)
        self.quit_hook(driver)

    def quit_hook(self, driver):
        s = input('quit(q): ')
        if s == 'q':
            driver.quit()

    def export_name(self, data):
        dataframe = pd.DataFrame({'name': data})
        dataframe.to_csv('dataset/name.csv')

    def read_name(self):
        dataset = pd.read_csv('dataset/name.csv', header=0)
        return dataset['name']

    def export_history_data(self):
        BaseUrl = 'https://coinmarketcap.com/currencies/{}/historical-data/'
        name_set = self.read_name()
        url_set = []
        for name in name_set:
            url_set.append(BaseUrl.format(name).replace(' ', '-'))
        print(url_set)

        # for url in url_set:
        #     driver = self.open_driver()
        #     driver.get(url)
        driver = self.open_driver()
        driver.get(url_set[2])
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/span/button').click()
        driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/div[2]/ul/li[2]').click()
        driver.find_element(By.XPATH, '/html/body/div/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/span/button').click()
        self.quit_hook(driver)

if __name__ == '__main__':
    test = CoinMarketCap()
    # test.download()
    test.export_history_data()
