import os
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

FRONT_PAGE = "https://djinni.co/jobs/?primary_keyword=QA&location=%D0%9A%D0%B8%D0%B5%D0%B2"
KEY = 'Python'


def init():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=os.path.abspath('c:\windows\system32\chromedriver'),
                              chrome_options=chrome_options)
    return driver


def tap_on_next_button(driver, url_links):
     driver.get(FRONT_PAGE)
     url_links = find_all_vacancies_on_page(driver, url_links)
     pager = driver.find_element_by_class_name('page-header').find_element_by_css_selector('h1').find_element_by_class_name('text-muted').text
     pages = int(int(pager)/15) + 1
     for i in range(2, pages):
         next_page = 'https://djinni.co/jobs/?page=' + str(i) + '&primary_keyword=QA&location=Киев'
         driver.get(next_page)
         url_links = find_all_vacancies_on_page(driver, url_links)
     return url_links


def jobs_db_init():
    conn = sqlite3.connect('jobs_djinni.sqlite')
    cur = conn.cursor()

    cur.execute('''DROP TABLE IF EXISTS Jobs''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Jobs
            (company TEXT, title TEXT,
             url TEXT)''')
    return conn


def find_all_vacancies_on_page(driver, url_links):
    job_list = driver.find_elements_by_class_name('list-jobs__title')
    for job in job_list:
        url_link = job.find_element_by_css_selector('a').get_attribute('href')
        url_links.append(url_link)
    return url_links

def company_name(driver):
    header = driver.find_element_by_class_name('page-header')
    company = header.find_element_by_css_selector('p').text
    return company


def job_title(driver):
    title = driver.find_element_by_class_name('page-header').find_element_by_css_selector('h1').text
    return title


def info_about_vacancy(driver, db, url_links):
    for link in url_links:
        driver.get(link)
        job_descriptions = driver.find_elements_by_class_name('profile-page-section')
        job_description_full = ''
        for job_description in job_descriptions:
            job_description_full = job_description_full + job_description.text
        if KEY in job_description_full:
            company = company_name(driver)
            title = job_title(driver)
            db.cursor().execute('''INSERT INTO Jobs (company, title, url) 
                                    VALUES (?, ?, ?)''', (company, title, link))
            db.commit()


def main():
    driver = init()
    jobs_db = jobs_db_init()
    url_links = []
    tap_on_next_button(driver, url_links)
    info_about_vacancy(driver, jobs_db, url_links)
    driver.quit()


if __name__ == "__main__":
    main()



