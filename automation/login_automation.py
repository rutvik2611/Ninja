from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginAutomation:
    def __init__(self, driver):
        # options = Options()
        # options.add_argument("--disable-blink-features=AutomationControlled")  # This will disable the property that Chrome uses to detect automation
        # options.add_argument("start-maximized")  # Start browser maximized
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")  # Set user agent to a common browser
        self.driver = driver

    def navigate_to_website(self, url):
        self.driver.get(url)

    def click_login_page_button(self, button_id):
        login_page_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, button_id)))
        login_page_button.click()

    def fill_login_form(self, username, password):
        username_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))
        password_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#passwd1")))
        username_field.send_keys(username)
        password_field.send_keys(password)