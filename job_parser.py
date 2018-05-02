import os
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FRONT_PAGE = "https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=QA"
KEY = 'Python'


def init():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path = os.path.abspath('c:\windows\system32\chromedriver'),
                              chrome_options=chrome_options)
    return driver


def tap_on_more_button(driver):
    driver.get(FRONT_PAGE)
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vacancyListId"]/div')))
            driver.find_element_by_link_text("Больше вакансий").click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vacancyListId"]/div')))
        except:
            break


def jobs_db_init():
    conn = sqlite3.connect('jobs.sqlite')
    cur = conn.cursor()

    cur.execute('''DROP TABLE IF EXISTS Jobs''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Jobs
            (company TEXT, title TEXT,
             url TEXT, address TEXT, address_url TEXT)''')
    return conn


def find_all_vacancies(driver):
    url_links = []
    job_list = driver.find_elements_by_class_name('vt')
    for job in job_list:
        url_links.append(job.get_attribute('href'))
    return url_links


def company_name(driver):
    company = driver.find_element_by_class_name('l-n').text
    company = company[:len(company) - 22]
    return company


def company_title(driver):
    title = driver.find_element_by_class_name('g-h2').text
    return title


def company_detail_screen(driver, company):
    address_info = []
    driver.find_element_by_partial_link_text(company).click()
    driver.get(driver.current_url + 'offices/')
    try:
        address = driver.find_elements_by_class_name('address')
        address = address[0].text
        address = address[:len(address) - 20]
        address_info.append(address)
        address_url = 'https://www.google.com.ua/maps/dir/Киев, ул. Драгоманова 40 з/Киев, ' + address
        address_info.append(address_url)
    except:
        address_info = []
        address_info.append('No address')
        address_info.append('')
    return address_info


def info_about_vacancy(driver):
    for link in find_all_vacancies(driver):
        driver.get(link)
        job_description = driver.find_element_by_class_name('b-vacancy').text
        if KEY in job_description:
            company = company_name(driver)
            title = company_title(driver)
            address_details = company_detail_screen(driver, company)
            address = address_details[0]
            address_url = address_details[1]

            jobs_db.cursor().execute('''INSERT INTO Jobs (company, title, url, address, address_url) 
                                    VALUES (?, ?, ?, ?, ?)''', (company, title, link, address, address_url))
            jobs_db.commit()


driver = init()
jobs_db = jobs_db_init()
tap_on_more_button(driver)
info_about_vacancy(driver)
driver.quit()



