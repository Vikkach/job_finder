import os
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FRONT_PAGE = "https://djinni.co/jobs/?primary_keyword=QA&location=%D0%9A%D0%B8%D0%B5%D0%B2"
KEY = 'Python'


def init():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=os.path.abspath('c:\windows\system32\chromedriver'),
                              chrome_options=chrome_options)
    return driver


def tap_on_next_button(driver):
     driver.get(FRONT_PAGE)
     try:
         wait = WebDriverWait(driver, 10)
         wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "вперед")))
         driver.find_element_by_partial_link_text("вперед").click()
         wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "вперед")))
     except:
         print('no next')


def jobs_db_init():
    conn = sqlite3.connect('jobs_djinni.sqlite')
    cur = conn.cursor()

    cur.execute('''DROP TABLE IF EXISTS Jobs''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Jobs
            (company TEXT, title TEXT,
             url TEXT)''')
    return conn


def find_all_vacancies(driver):
    url_links = []
    job_list = driver.find_elements_by_class_name('list-jobs__title')
    for job in job_list:
        url_links.append(job.get_attribute('href'))
    tap_on_next_button(driver)
    return url_links


def company_name(driver):
    company = driver.find_element_by_class_name('/html/body/div[1]/div[1]/p[1]').text
    return company


def job_title(driver):
    title = driver.find_element_by_class_name('page-header').get_attribute('h1')
    return title


def info_about_vacancy(driver):
    for link in find_all_vacancies(driver):
        driver.get(link)
        job_description = driver.find_element_by_class_name('profile-page-section').text
        if KEY in job_description:
            company = company_name(driver)
            title = job_title(driver)
            jobs_db.cursor().execute('''INSERT INTO Jobs (company, title, url) 
                                    VALUES (?, ?, ?)''', (company, title, link))
            jobs_db.commit()


driver = init()
jobs_db = jobs_db_init()
info_about_vacancy(driver)
driver.quit()



