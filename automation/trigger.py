import sys
from pathlib import Path



sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from automation.helper.helper import get_page_source
from automation.login_automation import LoginAutomation
from dotenv import load_dotenv
import os

from optimus_db.secure_rsa_db.fetch_latest_rsa import fetch_valid_rsa_value
from optimus_db.secure_rsa_db.update_status import update_attempt_status


def load_environment_variables():
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    return username, password

def fetch_rsa_value():
    secure_id = None
    while secure_id is None:
        try:
            secure_id = fetch_valid_rsa_value()
            print(secure_id)
        except ValueError as e:
            print(f"An error occurred while fetching the RSA value: {e}")
            print("Retrying...")
            break
    return secure_id

def create_driver():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-infobars")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    return driver

def automate_login(driver, username, password, secure_id):
    try:
        login_automation = LoginAutomation(driver)
        login_automation.navigate_to_website("https://myworkspace-cdc2-4.jpmchase.com/logon/LogonPoint/tmindex.html")
        login_automation.click_login_page_button("warnButton")
        get_page_source(driver, 'after_click')
        login_automation.fill_login_form(username, password, secure_id)

        login_automation.click_login_button()
        get_page_source(driver, 'after_login')
    except Exception as e:
        print("An error occurred in automated_login")
        raise Exception("automated_login Error -> " + str(e)) # re-raise the exception

def trigger(secure_id=None):
    try:
        username, password = load_environment_variables()
        if secure_id is None:
            secure_id = fetch_rsa_value()
        driver = create_driver()
        automate_login(driver, username, password, secure_id)
    except Exception as e:
        print(f"An error occurred in trigger")
        get_page_source(driver, 'after_exception')
        if driver is not None:
            driver.close()
            driver.quit()
        raise Exception("trigger Error -> " + str(e))# re-raise the exception

if __name__ == "__main__":
    try:
        # add_secure_rsa("33116837")
        trigger()
        update_attempt_status("success")
    except Exception as e:
        print(f"An error occurred: {e}")
        update_attempt_status("failure")