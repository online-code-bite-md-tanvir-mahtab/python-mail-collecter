from lib2to3.pgen2 import driver
from seleniumwire.undetected_chromedriver import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd


if __name__ == '__main__':
    # we need to ask for the web url link 
    while True:
        data = pd.read_csv('urls.csv')
        for url in data['url']:
            web_url_endpoint = url

            option = Options()
            option.headless = True
            driver = webdriver.Chrome(options=option)
            driver.maximize_window()
            driver.get(url=web_url_endpoint)


            body = driver.find_element(By.TAG_NAME,'body')

            html_page = driver.page_source
            driver.close()
            driver.quit()

            soup = BeautifulSoup(html_page,'html.parser')

            datas = []
            datas.append(soup.text)


            # now i am going to check for hte email in the data
            import re

            email_list = []
            for text in datas:
                email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",text)
                email_list.append(email)

            import pandas as pd
            email_data = pd.read_csv('email_data.csv')
            df = pd.DataFrame({
                'emails':[email_list]
            })
            if email_data.empty:
                df.to_csv('email_data.csv',index=False)
            else:
                df.to_csv('email_data.csv',index=False,header=False,mode='a')


        user_input_for_exit_or_continue = input("Enter yes to exit or no to continue the programm :").lower()
        if user_input_for_exit_or_continue == 'yes':
            break