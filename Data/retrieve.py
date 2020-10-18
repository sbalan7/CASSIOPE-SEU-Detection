import os
import requests
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def retrieve_omni_data():
    omni1 = 'http://omniweb.gsfc.nasa.gov/staging/omni2_daily_bEDz_O8ES5.lst'
    omni2 = 'http://omniweb.gsfc.nasa.gov/staging/omni2_daily_bEDz_O8ES5.fmt'
    start_date = '20131003'
    end_date = '20200930'

    driver = webdriver.Chrome(executable_path='C:\\Users\\sbala\\Documents\\chromedriver.exe')
    driver.maximize_window()
    driver.get('https://omniweb.gsfc.nasa.gov/form/dx1.html')

    driver.find_element_by_xpath("//input[@value='ftp']").click()
    driver.find_element_by_xpath("//input[@value='daily']").click()

    st = driver.find_element_by_name('start_date')
    st.send_keys(Keys.CONTROL, "a")
    st.send_keys(start_date)

    en = driver.find_element_by_name('end_date')
    en.send_keys(Keys.CONTROL, "a")
    en.send_keys(end_date)

    elements = [10,11,12,13,14,15,16,22,23,24,25,26,28,35,36,38,39,46,47,48,50,55]

    for element in elements:
        x_path = "//input[@value='{}']".format(str(element))
        driver.find_element_by_xpath(x_path).click()

    driver.find_element_by_xpath("//input[@value='Submit']").click()

    r = requests.get(omni1, allow_redirects=True)
    with open(os.path.join('Data', 'omni_data.txt'), 'wb') as f:
        f.write(r.content)

    r = requests.get(omni2, allow_redirects=True)
    with open(os.path.join('Data', 'omni_headers.txt'), 'wb') as f:
        f.write(r.content)

    driver.quit()

def retrieve_cassiope_data():
    cassiope = 'ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/CASSIPOE/CASSIOPE_Sub Data Set.csv'

    with urllib.request.urlopen(cassiope) as r:
        data = r.read()
        with open(os.path.join('Data', 'cassiope.txt'), 'wb') as f:
            f.write(data)    
    
