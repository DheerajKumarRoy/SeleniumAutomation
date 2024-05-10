from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pickle
from os.path import exists

filter = ['Python', 'RedHat', 'Linux MySQL', 'Docker', 'OpenShift', 'Kubernetes']
keys =''
for item in filter:
    keys+=item+'%20'
url = f'https://www.linkedin.com/search/results/people/?keywords={keys}&origin=GLOBAL_SEARCH_HEADER&page='

def main():
    global driver
    driver = webdriver.Chrome()
    login()
    send_connection_requests(url)

#LOGIN
def login():
    if not exists("cookies.pkl"):
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        username = "your username"
        password = "your password"
        driver.find_element("xpath", "//input[@name='session_key']").send_keys(username)
        driver.find_element("xpath", "//input[@name='session_password']").send_keys(password)
        time.sleep(2)
        submit = driver.find_element("xpath","//button[@type='submit']").click()
        cookies = driver.get_cookies()
        with open('cookies.pkl','wb')as file:
            pickle.dump(cookies,file)
        driver.get("https://www.linkedin.com/")
        time.sleep(2)
    else:
        driver.get("https://www.linkedin.com/login/")
        with open('cookies.pkl','rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
                time.sleep(2)

#send_connection_requests
def send_connection_requests(url):
    for i in range(1,50):
        driver.get(url+str(i))

        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]
        if connect_buttons:
            for btn in connect_buttons:
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(2)
                send = driver.find_element(By.XPATH, "//button[@aria-label='Send without a note']")
                driver.execute_script("arguments[0].click();", send)
                close = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                driver.execute_script("arguments[0].click();", close)
                time.sleep(2)
        else:
            continue
main()
