import time

from automation.helper.helper import log_function_name
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginAutomation:
    # logger = logging.getLogger(__name__)
    def __init__(self, driver):
        # options = Options()
        # options.add_argument("--disable-blink-features=AutomationControlled")  # This will disable the property that Chrome uses to detect automation
        # options.add_argument("start-maximized")  # Start browser maximized
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")  # Set user agent to a common browser
        self.driver = driver


    @log_function_name
    def navigate_to_website(self, url):
        self.driver.get(url)

    @log_function_name
    def click_login_page_button(self, button_id):
        login_page_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, button_id)))
        login_page_button.click()

    @log_function_name
    def fill_login_form(self, username, password, secure_id):
        print(f"Username: {username}")
        # print(f"Password: {password}")
        print(f"Secure ID: {secure_id}")
        if username is None or password is None or secure_id is None:

            raise ValueError("username, password, and secure_id must not be None")

        username_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login")))
        password_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "passwd1")))
        secure_id_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "passwd")))

        username_field.send_keys(username)
        password_field.send_keys(password)
        secure_id_field.send_keys(secure_id)

    @log_function_name
    def click_login_button(self):
        login_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "loginBtn")))
        login_button.click()

        # Wait for the page to load
        time.sleep(2)

            # Check for the error messages
        error_messages = [
            "Your ID, password or SecurID passcode was incorrectly entered. Please re-enter your credentials after your SecurID token has cycled to the next set of digits",
            "Hello, additional information is required about your account."
        ]

        for error_message in error_messages:
            if error_message in self.driver.page_source:
                print("Login failed: " + error_message)
                raise Exception("Login failed: " + error_message)