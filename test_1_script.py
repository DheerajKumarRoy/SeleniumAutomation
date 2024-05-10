from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from os import makedirs
from time import strftime, sleep

file_urls = 'https://www.getcalley.com/page-sitemap.xml'

# Resolutions to be tested
DeskRes = {'res1': '1920x1080', 'res2': '1366x768', 'res3': '1536x864'}
MobRes = {'res1': '360x640', 'res2': '414x896', 'res3': '375x667'}
# List of all resolutions
AllRes = {'Desktop': DeskRes, 'Mobile': MobRes}


def chrome():
    driver = webdriver.Chrome()
    DriverSpecifier(driver)
    driver.quit()

def firefox():
    driver = webdriver.Firefox()
    DriverSpecifier(driver)
    driver.quit()

def edge():
    driver = webdriver.Edge()
    DriverSpecifier(driver)


def DriverSpecifier(driver):
    driver.get(file_urls)
    a_tags = driver.find_elements(By.XPATH, '//table[@id="sitemap"]//a')
    urls = [url.get_attribute('href') for index, url in enumerate(a_tags) if index < 5]
    for key, value in AllRes.items():
        Device = key
        resolutions = value
        Tester(resolutions, urls, Device, driver)

def Tester(resolutions, urls, Device, driver):
    for key, value in resolutions.items():
        try:
            resolution = value.split('x')
            driver.set_window_size(resolution[0], resolution[1])
            driver.set_window_position(0, 0)
            browser = driver.capabilities['browserName']
            makedirs(f'{browser}/{Device}/{value}', exist_ok=True)
            for url in urls:
                try:
                    time_stamp = strftime('%d_%m_%y-%H_%M_%S')
                    global log
                    log = f'{time_stamp} {browser} {value} {url}'
                    driver.get(url)
                    log = log + ' successful!'
                    path = f'{browser}/{Device}/{value}/screenshot-{time_stamp}.png'
                    driver.save_screenshot(path)
                except Exception as e:
                    log = log + f' {e}'
                finally:
                    with open('log.txt', 'a') as logs:
                        logs.write(log+'\n')
        except Exception as e:
            log = log + f' {e}'
            with open('log.txt', 'a') as logs:
                logs.write(log+'\n')
        finally:
            with open('log.txt', 'a') as logs:
                logs.write('\n')

# chrome()
# firefox()
edge()
