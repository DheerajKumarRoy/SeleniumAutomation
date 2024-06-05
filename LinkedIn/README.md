
# LinkedIn Automation with Selenium

Welcome to the LinkedIn Automation Repository! This project provides various automated LinkedIn tasks using Selenium.

## Features

- **Automated Login**: Log into LinkedIn using provided credentials.
- **Connection Requests**: Send connection requests automatically based on specified search keywords.
- **Withdraw Connection Requests**: Withdraw the last n pages of connection requests.
- **Web Scraping**: Scrape user data from all LinkedIn connections.
- **Send Messages**: Send messages to your LinkedIn connections.
- **Save Data to Excel**: Save scraped data to an Excel file.
- **Send Email**: Send emails to all the email addresses in the database scraped from LinkedIn.

## Requirements

- Python 3.6+
- Selenium
- ChromeDriver

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/DheerajKumarRoy/SeleniumAutomation.git
cd SeleniumAutomation/LinkedIn
```

2. **Install the required packages:**

```bash
pip install -r requirements.txt
```

3. **Download and install ChromeDriver:**

Ensure that the ChromeDriver version matches your installed Chrome browser version. Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Configuration

Before running the script, set up your LinkedIn credentials and the path to your ChromeDriver in a configuration file named `config.py` or via environment variables:

```python
# config.py
from os import environ

config = {}
config['WEB_DRIVER_PATH'] = ''  # specify WEB_DRIVER_PATH or set it as an empty string if the driver is in the same directory as python
config['LINKEDIN_USERNAME'] = environ.get('LINKEDIN_USERNAME')
config['LINKEDIN_PASSWORD'] = environ.get('LINKEDIN_PASSWORD')
```

## Usage

### Running the Automation Script

To run the main automation script:

```python
from linkedin import config
from linkedin import SEND_CONNECTON
from linkedin import WITHDRAW_CONN_REQ
from linkedin import WEB_SCRAPER
from linkedin import SEND_MESSAGES
from linkedin import save_as_excel
from send_email import SEND_EMAIL
from search_keys import SEARCH_KEYS
from os import environ

# LinkedIn credential & webdriver_path configuration
config['WEB_DRIVER_PATH'] = '' 
config['LINKEDIN_USERNAME'] = environ.get('LINKEDIN_USERNAME')
config['LINKEDIN_PASSWORD'] = environ.get('LINKEDIN_PASSWORD')

# Withdraw the last n pages of connection requests
withdraw = WITHDRAW_CONN_REQ()

# Scrape user data from all LinkedIn connections
scraper = WEB_SCRAPER()

# Send connection requests based on search keywords
send_connection = SEND_CONNECTON(SEARCH_KEYS, (2, 5))

# Send a message to connections
msg = 'this is a test message!'
send_message = SEND_MESSAGES(msg)

# Send email to all emails in the database
send_mail = SEND_EMAIL()

# Save database to an Excel file
excel_data = save_as_excel()
```

## Script Overview

- `WITHDRAW_CONN_REQ(n)`: Withdraws the last n pages of connection requests.
- `WEB_SCRAPER()`: Scrapes user data from all LinkedIn connections.
- `SEND_CONNECTON(search_keywords, (num_requests, num_keywords))`: Sends connection requests based on search keywords.
- `SEND_MESSAGES(message)`: Sends a message to connections.
- `SEND_EMAIL()`: Sends emails to all email addresses in the database.
- `save_as_excel()`: Saves scraped data to an Excel file.

## Contributing

We welcome contributions! Feel free to open an issue or submit a pull request for any improvements or additional features you would like to see.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for more details.

## Disclaimer

This project is for educational and research purposes only. Use it responsibly and in accordance with LinkedIn's terms of service. The author is not responsible for any misuse of this tool.

## Contact

For any questions or support, please open an issue on GitHub or contact [dheerajkumarroy@gmail.com](mailto:dheerajkumarroy@gmail.com).

Thank you for using LinkedIn Automation! Happy networking!
