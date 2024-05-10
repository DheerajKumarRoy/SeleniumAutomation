# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

driver = webdriver.Chrome()
driver.set_window_size(width=1366,height=768)
driver.set_window_position(0,0)
Option = Options()
Option.add_argument('--disable-notifications')

# %%

Username = 'prexo.mis@dealsdray.com'
Password = 'prexo.mis@dealsdray.com'

driver.get('https://demo.dealsdray.com/')
sleep(0.5)


# %%
driver.find_element(By.XPATH,'//input[@name="username"]').send_keys(Username)
driver.find_element(By.XPATH,'//input[@name="password"]').send_keys(Password)
sleep(0.5)
driver.find_element(By.XPATH,'//button[@type="submit"]').click()
sleep(0.5)
    # input()

# %%
menu = driver.find_elements(By.TAG_NAME,'button')
for index,but in enumerate(menu):
    print(but.text,index)
    if but.text=='menu':
        but.click()
sleep(1)

# %%

order = driver.execute_script("return document.getElementsByTagName('button')")[1].click()
sleep(1)

# %%

BulkOrders = driver.execute_script("return document.getElementsByTagName('button')[1]").click()
sleep(1)

# %%

file = "C:/Users/Dheeraj/Desktop/demo-data.xlsx"

input = driver.find_element(By.TAG_NAME,'input').send_keys(file)
sleep(1)


# %%

Import = driver.find_elements(By.TAG_NAME,'button')[2].click()
sleep(1)


# %%
validateData = driver.find_elements(By.TAG_NAME,'button')[2].click()
sleep(1)


# %%
try:
    #any error to skip notification which can't be closed with selenium
    validateData = driver.find_elements(By.TAG_NAME,'button').click()
    

except Exception as e:
    print('''intentional error to skip notification which can't be closed with selenium''')
    sleep(1)

finally:
    driver.save_screenshot('screenshot.png')
    sleep(1)
    submit = driver.find_elements(By.TAG_NAME,'button')[2].click()
    sleep(10)
    driver.quit()


