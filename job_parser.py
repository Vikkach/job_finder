import os  
import sqlite3
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options

FRONT_PAGE = "https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=QA"
KEY = 'Python'


chrome_options = Options()  
chrome_options.add_argument("--headless")  

driver = webdriver.Chrome(executable_path=os.path.abspath('c:\windows\system32\chromedriver'),   chrome_options=chrome_options)  
driver.get(FRONT_PAGE)

url_links = []
job_list = driver.find_elements_by_class_name('vt')
for job in job_list:
    url_links.append(job.get_attribute('href'))


for link in url_links:
    driver.get(link)
    job_list = []
    job_description = driver.find_element_by_class_name('b-vacancy').text
    if 'Python' in job_description:
        company = driver.find_element_by_class_name('l-n').text
        title = driver.find_element_by_class_name('g-h2').text
        
        
        conn = sqlite3.connect('jobs.sqlite')
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Jobs
                    (id INTEGER UNIQUE, company TEXT, title TEXT,
                     url TEXT)''')
        cur.execute('''INSERT INTO Jobs (company, title, url) VALUES (?, ?, ?)''', (company, title, link))
        conn.commit()
        print('------')

#print(url_links)


