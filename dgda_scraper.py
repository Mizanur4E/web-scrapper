import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.chrome.service import Service
from os import listdir
from bs4 import BeautifulSoup
from os.path import isfile, join
import warnings

warnings.filterwarnings("ignore")


def scrape_pages_and_get_dataframe(page, bs_data=None):
    browser = webdriver.Chrome(executable_path="./chromedriver")
    column_names = ['sl_center', 'Name_of_the_Pharmaceutical', 'Brand_Name', 'Generic_Name', 'Strength',
                    'Dosages', 'PRICE', 'Use_for', 'DAR']
    df_main = pd.DataFrame(columns=column_names)
    browser.get(page)
    while True:
        # print(current, previous)
        browser.find_element_by_id("gridData_next").click()
        time.sleep(1)
        source_data = browser.page_source
        bs_data = bs(source_data, 'html.parser')
        flag = bs_data.find_all('a', {'id': 'gridData_last'})[0].get("class")[-1]
        df = extract_data_from_html(bs_data)
        df_main = df_main.append(df)
        if flag == 'ui-state-disabled':
            print(flag)
            break
    browser.close()
    return df_main


def extract_data_from_html(soup):
    column_names = ['sl_center', 'Name_of_the_Pharmaceutical', 'Brand_Name', 'Generic_Name', 'Strength',
                    'Dosages', 'PRICE', 'Use_for', 'DAR']
    df = pd.DataFrame(columns=column_names)
    table_rows = soup.find("tbody").find_all("tr")
    for row in table_rows:
        df = df.append({'sl_center': row.find("td", {"class": "sl center"}).get_text(),
                        'Name_of_the_Pharmaceutical': row.find("td",
                                                               {"class": "Name of the Pharmaceutical"}).get_text(),
                        'Brand_Name': row.find("td", {"class": "Brand Name"}).get_text(),
                        'Generic_Name': row.find("td", {"class": "Generic Name"}).get_text(),
                        'Strength': row.find("td", {"class": "Strength"}).get_text(),
                        'Dosages': row.find("td", {"class": "Dosages"}).get_text(),
                        'PRICE': row.find("td", {"class": "PRICE"}).get_text(),
                        'Use_for': row.find("td", {"class": "Use for"}).get_text(),
                        'DAR': row.find("td", {"class": "DAR"}).get_text()}, ignore_index=True)
    return df


def main(page_name):
    df_main = scrape_pages_and_get_dataframe(page_name)
    df_main.to_csv("dgda_extracted_data.csv")


if __name__ == '__main__':
    main("http://dgdagov.info/index.php/registered-products/allopathic")
