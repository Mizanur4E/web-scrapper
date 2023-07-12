from selenium import webdriver
import bs4
import pandas as pd
import time


def scrapping_generic_info():
    """Extract information of generics listed on ith page"""
    browser = webdriver.Firefox()
    generic = pd.DataFrame(columns=['Generic_name', 'Indications', 'Side_effects', 'Therapeutic_class'])
    brand_table = pd.DataFrame(columns=['Brand_name', 'Dosage', 'Strength', 'Company', 'Generic_name'])

    # med ex has total 78 page of generic names.
    for i in range(10, 20):

        browser.get(f'https://medex.com.bd/generics?page={i}')
        soup = bs4.BeautifulSoup(browser.page_source)
        all_generic_page = soup.find_all("a", {"class": "hoverable-block darker"})

        for element in all_generic_page:
            generic_link = element.get("href")
            browser.get(generic_link)
            soup = bs4.BeautifulSoup(browser.page_source)

            med_genericName = soup.find("h1", {"class": "page-heading-1-l"}).get_text()
            all_sections = soup.find_all("div", {"class": "ac-body"})
            all_headers = soup.find_all("h4", {"class": "ac-header"})
            i = 0
            print(len(all_sections))
            parts = [None] * len(all_sections)
            for sections in all_sections:

                parts[i] = sections.get_text()
                headers = all_headers[i].get_text()
                # print(headers)
                if headers == 'Therapeutic Class':
                    med_therapeuticClass = parts[i]
                    # print(med_therapeuticClass)
                if headers == 'Side Effects':
                    med_sideEffects = parts[i]
                    # print(med_sideEffects)

                i = i + 1
                med_indications = parts[0]
                # med_sideEffects=parts[4]
                # med_therapeuticClass=parts[8]
            generic = generic.append(
                {'Generic_name': med_genericName, 'Indications': med_indications, 'Side_effects': med_sideEffects,
                 'Therapeutic_class': med_therapeuticClass}, ignore_index=True)

            brands = browser.find_element_by_css_selector('a.hidden-xs')
            brands.click()

            for i in range(350):
                try:
                    Brand = browser.find_element_by_css_selector(
                        'tr.brand-row:nth-child(' + str(i + 1) + ') > td:nth-child(1)').text
                    Dosage = browser.find_element_by_css_selector(
                        'tr.brand-row:nth-child(' + str(i + 1) + ') > td:nth-child(2)').text
                    Strength = browser.find_element_by_css_selector(
                        'tr.brand-row:nth-child(' + str(i + 1) + ') > td:nth-child(3)').text
                    Comapny = browser.find_element_by_css_selector(
                        'tr.brand-row:nth-child(' + str(i + 1) + ') > td:nth-child(4)').text
                    brand_table = brand_table.append(
                        {'Brand_name': Brand, 'Dosage': Dosage, 'Strength': Strength, 'Comapny': Comapny,
                         'Generic_name': med_genericName}, ignore_index=True)
                    time.sleep(2)

                except:

                    print('One Brand missing')
                    pass

    generic.to_csv('generic10_20.csv')
    brand_table.to_csv('brands10_20.csv')


def main() -> object:
    scrapping_generic_info()


if __name__ == '__main__':
    main()
