from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helper.helper import get_page_source
from login_automation import LoginAutomation
from dotenv import load_dotenv
import os

from optimus_db.secure_rsa_db.fetch_latest_rsa import fetch_valid_rsa_value

load_dotenv()

# Load username and password from environment variables
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
secure_id = None
while secure_id is None:
    try:
        secure_id = fetch_valid_rsa_value()
        print(secure_id)
    except ValueError as e:
        print(f"An error occurred while fetching the RSA value: {e}")
        print("Retrying...")

# Create a new instance of the Chrome driver and keep it open after the script finishes
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Create an instance of the LoginAutomation class
login_automation = LoginAutomation(driver)

# Save the HTML source of the current page to a file
# get_page_source(driver, 'homepage')

# Use the methods of the LoginAutomation class to automate the login process
login_automation.navigate_to_website("https://myworkspace-cdc2-4.jpmchase.com/logon/LogonPoint/tmindex.html")
login_automation.click_login_page_button("warnButton")
# Save the HTML source of the redirected page to a file
get_page_source(driver, 'after_click')
login_automation.fill_login_form(username, password, secure_id)

# Click the login button
login_automation.click_login_button()

# Save the HTML source of the page after login to a file
get_page_source(driver, 'after_login')