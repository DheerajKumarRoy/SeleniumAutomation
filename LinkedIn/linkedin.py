from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pickle
from os.path import exists

#credentials
config = {}


#LOGIN
def login():    
    global driver
    driver = webdriver.Chrome(config['WEB_DRIVER_PATH'])
    driver.maximize_window()
    if not exists("linkedin_cookies.pkl"):
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        username =config['LINKEDIN_USERNAME']
        password = config['LINKEDIN_PASSWORD']
        driver.find_element("xpath", "//input[@name='session_key']").send_keys(username)
        driver.find_element("xpath", "//input[@name='session_password']").send_keys(password)
        time.sleep(2)
        submit = driver.find_element("xpath","//button[@type='submit']").click()
        time.sleep(3)
        cookies = driver.get_cookies()
        with open('linkedin_cookies.pkl','wb') as file:
            pickle.dump(cookies,file)
        driver.get("https://www.linkedin.com/")
        time.sleep(2)
    else:
        driver.get("https://www.linkedin.com/login/")
        with open('linkedin_cookies.pkl','rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        time.sleep(2)
        # driver.get("https://www.linkedin.com/")

class WEB_SCRAPER:
    def __init__(self):
        #login
        login()
        profile_urls = self.getURLs()
        total = len(profile_urls.copy())
        import sqlite3
        conn = sqlite3.connect('webSrapper.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Profile FROM webdata')
        existings = cursor.fetchall()
        conn.close()
        for item in existings:
            profile = f'https://www.{item[0]}/'
            if profile in profile_urls:
                profile_urls.remove(profile)
        print('new profiles: ',len(profile_urls))

        # Print the URLs
        for  url in profile_urls:
            data = ''
            driver.get(url + 'overlay/contact-info/')
            time.sleep(2)
            info = driver.execute_script('return document.getElementsByClassName("pv-profile-section__section-info section-info")')
            for details in info:
                data+=details.text
            total_saved = self.dbIntigration(data)
            data = ''
            print(f'profiles scraped: {total_saved} of {total}')
        driver.quit()

    #get profiles
    @staticmethod
    def getURLs():
        # Navigate to the My Network page
        driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

        # Wait for the connections page to load
        time.sleep(5)

        # # Scroll to the bottom of the page to load all connections
        scroll_pause_time = 5  # Pause time between scrolls
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            try:
                # Scroll down to the bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait to load page
                time.sleep(scroll_pause_time)
                

                btns = driver.find_elements(By.TAG_NAME, "button")
                if btns:
                    for btn in btns:
                        if btn.text=='Show more results':
                            driver.execute_script("arguments[0].click();", btn)
                            # Wait to load page
                time.sleep(scroll_pause_time)
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break
                last_height = new_height
            except Exception as e:
                print(e)
                continue


        # Find all the connection elements
        connections = driver.find_elements(By.XPATH, '//a[@class="ember-view mn-connection-card__link"]')

        # Extract the URLs
        profile_urls = [conn.get_attribute('href') for conn in connections if conn.get_attribute('href')]
        print('total profiles: ', len(profile_urls))
        return profile_urls
    
    #prosecess data
    def dataProcess(self,data):
        db = dict()
        user = dict()
        data = data.strip().splitlines()
        field = ['Profile','Name','Website','Phone','Email','Address','IM','Birthday']
        for index, entry in enumerate(data):
            for item in field:
                if item in entry:
                    db[item]=index+1
                elif 'Profile' in entry:
                    user['Name'] =entry.split('’s')[0]
                
                else:
                    continue
        for key,value in db.items():
            if ' ' in data[value]:
                user[key]=data[value]
            else:
                user[key]=data[value]
        print('data scrapped: ', user)
        return user

    #store enteries to db
    def dbIntigration(self,data):
        user = self.dataProcess(data)
        
        keys = tuple(user.keys())
        values = tuple(user.values())

        import sqlite3
        conn = sqlite3.connect('webSrapper.db')
        cursor = conn.cursor()

        #create a table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS webdata
                (
                    Profile TEXT PRIMARY KEY,
                    NAME TEXT,
                    Website TEXT,
                    Phone INTEGER,
                    Email TEXT,
                    Address TEXT,
                    IM TEXT,
                    Birthday TEXT
                )
        ''')

        #INSERT VALUES
        cursor.execute(f'''
        INSERT OR IGNORE INTO webdata
                {keys} VALUES {values}
        ''')

        conn.commit()
        cursor.execute('SELECT * FROM webdata')
        data = cursor.fetchall()
        if data:
            data = len(data)
        else:
            data = None
        conn.close()
        #print('profiles scraped: ',data)
        return data

class SEND_CONNECTON:
    def __init__(self,keys,num):  #takes a list of keys and a list or tupple of (num of connections, num of keys to be used)
         #login
        login()
        #send connections
        self.send_connection_requests(keys,num)
        driver.quit()

    #send_connection_requests
    def send_connection_requests(self,keys,num):
        num_conn, num_keys = num
        from random import sample
        filter = sample(keys,num_keys)
        key =''
        for item in filter:
            key+=item+'%20'
        url = f'https://www.linkedin.com/search/results/people/?geoUrn=%5B"102713980"%5D&keywords={key}&page='
        n=0
        while True:
            print('Keys: ',filter)
            if n==num_conn:
                print(f'connection requests sent: {n} ')
                break
            for i in range(1,100):
                try:
                    if n==num_conn:
                        break
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
                            n+=1
                            time.sleep(2)
                            print(f'connection requests sent: {n} of {num_conn}')
                            if n==num_conn:
                                break
                    else:
                        h2_tags = driver.find_elements(By.TAG_NAME, "h2")
                        if [tag for tag in h2_tags if tag.text=='No results found']:
                            filter = sample(keys,num_keys)
                            key =''
                            for item in filter:
                                key+=item+'%20'
                            break
                        else:
                            continue
                except Exception as e:
                    print(e)
                    continue

class WITHDRAW_CONN_REQ:
    def __init__(self,num):
        login()
        self.withdraw_requests(num)
        driver.quit()
    
    #num is number of pages to be dealth with from last
    def withdraw_requests(self,num):
        driver.get('https://www.linkedin.com/mynetwork/invitation-manager/sent/')
        pages = driver.find_elements(By.TAG_NAME,'button')
        last_page = [btn.text for btn in pages if btn.text.isdigit()]
        n=int()
        if last_page:
            n = int(last_page[-1])
        else:
            n=1
        if num>=n:
            num=n-1
        url = 'https://www.linkedin.com/mynetwork/invitation-manager/sent/?page='
        for i in range(n-num,n+1):
            driver.get(url+str(i)) #remove n- if error occurs
            btns = driver.find_elements(By.TAG_NAME,'button')
            withdraw_btns = [btn for btn in btns if btn.text=='Withdraw']
            # driver.execute_script("arguments[0].click();", withdraw_btns[0])
            if withdraw_btns:
                for btn in withdraw_btns:
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)
                    btns =  driver.find_elements(By.TAG_NAME,'button')
                    withdraw_btn = [btn for btn in btns if btn.text=='Withdraw'][0]
                    driver.execute_script("arguments[0].click();", withdraw_btn)
                    time.sleep(1)
            else:
                continue

class SEND_MESSAGES:
    def __init__(self,msg):
        login()
        profiles = WEB_SCRAPER.getURLs()
        black_list = ['url1','url2']
        profile_url = [url for url in profiles if not any(link in url for link in black_list)]
        for url in profile_url:
            self.send(url,msg)

    def send(self, url,msg):
        driver.get(url)
        time.sleep(1)
        btns = driver.find_elements(By.TAG_NAME, 'button')
        msg_btn = [btn for btn in btns if btn.text=='Message']
        if msg_btn:
            driver.execute_script("arguments[0].click();", msg_btn[0])

            # activate msg div
            div = driver.find_elements(By.XPATH, '//div[@aria-label="Write a message…"]')[0].click()

            # find p tags in text box
            p_tags = driver.find_elements(By.XPATH, '//div[@aria-label="Write a message…"]//p')
            n=1
            for btn in p_tags:
                if n==len(btns):
                    btn.send_keys(msg)
                else:
                    driver.execute_script("arguments[0].innerText='';", btn)
                n+=1
            send = driver.find_element(By.XPATH, '//button[text()="Send"]')
            driver.execute_script("arguments[0].click();",send)
        time.sleep(1)

def save_as_excel():
    import pandas as pd
    import sqlite3
    conn = sqlite3.connect('webSrapper.db')
    query = 'SELECT * FROM webdata'
    df = pd.read_sql_query(query,conn)
    df.to_excel('linkedin_data.xlsx',index=True,engine='openpyxl')
    conn.close()
