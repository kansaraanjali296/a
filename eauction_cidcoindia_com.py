import os
import re
import shutil
import sqlite3
import time
import glob
import warnings
from urllib import response
import pyodbc
import requests
import logging
from zipfile import ZipFile
import urllib.request
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def download_file_dir(url):
    files_dir = os.path.expanduser('~') + "\\Documents\\" + "PythonDocuments\\" + url.split('://')[1].split("/")[0] + "_py\\" + 'File'
    if os.path.exists(files_dir):
        pass
    else:
        os.makedirs(files_dir)
    return files_dir


def temp_file_dir():
    temp_dir_Name = os.path.abspath('Temp')
    # temp_dir_Name = os.chdir('/Temp')
    if os.path.exists(temp_dir_Name):
        pass
    else:
        os.makedirs(temp_dir_Name)
    return temp_dir_Name

try:

    url = 'https://eauction.cidcoindia.com/'
    temp_dir_Name = temp_file_dir()

    # create Temp folder for save downloaded files
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {"download.default_directory": temp_dir_Name})

    warnings.simplefilter("ignore")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    while True:
        driver.get(url)
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@class="btn btn-sm"]').click()

        # driver.find_element(By.XPATH, '//*[@id="liveTendersAuctions"][1]').click()
        # time.sleep(2)
        tr_all_data = driver.find_elements(By.XPATH, "//*[@id='liveTenders']//table/tbody//tr")

        for tr_data in tr_all_data:
            time.sleep(1)
            Tender_number = tr_data.find_element(By.XPATH, ".//td[1]").text
            print(Tender_number)
            Tender_Notice_No = tr_data.find_element(By.XPATH, ".//td[2]").text
            Tender_Summery = tr_data.find_element(By.XPATH, './/td[3]').text
            Bid_deadline_2 = tr_data.find_element(By.XPATH, './/td[5]').text.split()[0]
            Bid_deadline_2 = datetime.strptime(Bid_deadline_2, '%Y-%m-%d').strftime('%d/%m/%Y')

            all_links = tr_data.find_elements(By.XPATH, ".//td[3]/a")
            for i in all_links:
                i.send_keys(Keys.CONTROL + Keys.RETURN)
                time.sleep(8)

                DocFees = i.find_element(By.XPATH, '//*[@id="tenderReport"]/div[4]//*[@class="form-group col-sm-12"]/label[2]').text
                EMD = i.find_element(By.XPATH, '//*[@id="tenderReport"]/div[4]//*[@class="form-group col-sm-12"]/label[4]').text
                OpeningDate = i.find_element(By.XPATH, '//*[@id="tenderReport"]/div[3]/div[3]/div[2]/div[6]/label[2]').text.split()[0]

                try:
                    links = driver.find_element(By.XPATH, '//*[@id="tenderDocumentContainer"]/div[2]/div/div[1]/div[1]/table/tbody/tr/td[5]').click()
                    time.sleep(5)

                    driver.implicitly_wait(5)
                    if links == None:
                        links = ''
                except:
                    links = ''

                list_of_files = glob.glob('Temp/*')
                latest_file = max(list_of_files, key=os.path.getctime)
                latest_file = latest_file.replace('.crdownload', '')
                print(latest_file, '1111111111111111111111')
                time.sleep(5)
                # latest_file = os.path.join(temp_dir_Name, (datetime.now().strftime(f"%d%m%Y_%H%M%S%f") + "." + latest_file.split(".")[1].replace('.crdownload', '')))

                fullname = datetime.now().strftime(f"%d%m%Y_%H%M%S%f") + "." + latest_file.split(".")[1]
                fullname = str(fullname)
                print(fullname, "4444444444444444444444444444444")


                files_dir = download_file_dir(url)
                print(files_dir, '222222222222222222222222')

                # f_n = os.rename(latest_file, fullname)
                # print(f_n, '333333333333333333333333333')

                # f_name = shutil.move(f_n, files_dir)
                # print(f_name, '44444444444444444444')

                # shutil.move(f_name, files_dir)
                # source = 'C:/Users/sai mohan pulamolu/Desktop/deleted/source/'cmd
                # destination = 'C:/Users/sai mohan pulamolu/Desktop/deleted/destination/'
                # allfiles = os.listdir(fullname)
                #
                # for f in allfiles:
                #     shutil.move(fullname + f, files_dir + f)

                shutil.move(latest_file, files_dir)

                driver.find_element(By.XPATH, '//*[@id="id19e"]/div/div[1]//*[@data-dismiss="modal"]').click()

        url = driver.find_element(By.XPATH, '//*[@id="id6f"]/tfoot//*[@id="id14"]').get_attribute('href')
        print(url)

        # allfiles = os.listdir(source)
        #
        # for f in allfiles:
        #     os.rename(source + f, destination + f)

        time.sleep(2)
        driver.implicitly_wait(0.5)
        if url == None:
            break
    driver.quit()

except Exception as e:
    print(e)

