from linkedin import config
from linkedin import SEND_CONNECTON
from linkedin import WITHDRAW_CONN_REQ
from linkedin import WEB_SCRAPER
from linkedin import SEND_MESSAGES
from linkedin import save_as_excel
from send_email import SEND_EMAIL
from search_keys import SEARCH_KEYS
from os import environ

# #linkedin credential & webdriver_path configuration
# #specify WEB_DRIVER_PATH or set it an empty string (if driver is in the same directory as python)
config['WEB_DRIVER_PATH'] = '' 
config['LINKEDIN_USERNAME'] =  environ.get('LINKEDIN_USERNAME')
config['LINKEDIN_PASSWORD'] = environ.get('LINKDEIN_PASSWORD')

# #WITHDRAW_CONN_REQ takes a parameter n for withdrawing last n pages requests
# withdraw = WITHDRAW_CONN_REQ()

# WEB_SCRAPER scrape user data from all the linkedin connectons
# scraper = WEB_SCRAPER()

# #SEND_CONNECTON takes two parameters (list of search keywords, tupple/list of (num of request, num of keywords) )
# send_connection = SEND_CONNECTON(SEARCH_KEYS,(2,5))


# #SEND_MESSAGES takes just a parameter msg to be sent
# msg = 'this is a test message!'
# send_message = SEND_MESSAGES(msg)

# #SEND_EMAIL takes nothing it sends email to all the emails in db scrapped from linkedin
#send_mail = SEND_EMAIL() 

# #saves db to excel file
# excel_data = save_as_excel()