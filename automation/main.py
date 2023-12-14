from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from login_automation import LoginAutomation
from dotenv import load_dotenv
import os

load_dotenv()

# Load username and password from environment variables
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# Create a new instance of the Chrome driver and keep it open after the script finishes
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Create an instance of the LoginAutomation class
login_automation = LoginAutomation(driver)

# Use the methods of the LoginAutomation class to automate the login process
login_automation.navigate_to_website("https://myworkspace-car-1.jpmchase.com/logon/LogonPoint/tmindex.html")
login_automation.click_login_page_button("warnButton")
login_automation.fill_login_form(username, password)