'''Module for cloning Ticket: ASCSWTEST-49'''
import unittest
import time
# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
# import resources to login to JIRA
import jtc_resource

class cloneticket(unittest.TestCase):
    # open url using selenium to get access to jira to clone
    # the template ASCSWTEST-49. Thats needed because the jira api
    # does not provide a clone ticket access

    baseUrl = "https://jira-test1.elektrobit.com/browse/ASCSWTEST-49"

    def setUp(self):
        # setup environment for Selenium
        self.baseUrl = "https://jira-test1.elektrobit.com/browse/ASCSWTEST-49"
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(0.2)
        self.driver.get(self.baseUrl)

    def test_runner(self):
        # Selenium runner for cloning tickets
        self.baseUrl = "https://jira-test1.elektrobit.com/browse/ASCSWTEST-49"
        self.driver.get(self.baseUrl)
        usr = jtc_resource.usr["usr"]
        password = jtc_resource.pw["pw"]
        try:
            usr_input = self.driver.find_element (
                                                 By.XPATH,
                                                 "/html/body/div[1]/div/div/div"
                                                 + "/main/form/div[1]/div[2]/div"
                                                 + "/div[1]/input",
                                                 )
            usr_input.send_keys(usr)
            time.sleep(0.5)
        except TimeoutException as error:
            error = "An Error occured at sending username"
            print(error)
        try:
            pw_input = self.driver.find_element(
                By.CSS_SELECTOR,
                "#login-form-password",
            )
            pw_input.send_keys(password)
            time.sleep(0.5)
        except TimeoutException as error:
            error = "An Error occured at sending password"
            print(error)
        try:
            login_btn = self.driver.find_element (
                                                 By.XPATH,
                                                 "/html/body/div[1]/div/div"
                                                 + "/div/main/form/div[2]/div/input",
                                                 )
            login_btn.click()
            time.sleep(0.5)
            self.assertIn("EB external Jira",self.driver.title)
        except TimeoutException as error:
            error = "An Error occured by clicking the login button"
            print(error)
        try:
            more_btn = self.driver.find_element (
                                                By.XPATH,
                                                "/html/body/div[1]/div[2]/div[1]"
                                                + "/div/div/main/div/div[2]/div"
                                                + "/header/div/div[2]/div/div/div"
                                                + "/div[1]/div[3]/a[2]/span",
                                                )
            more_btn.click()
            time.sleep(0.5)
        except TimeoutException as error:
            error = "An Error occured by clicking the more button"
            print(error)
        try:
            clone_btn = self.driver.find_element (
                                                 By.XPATH,
                                                 "/html/body/div[1]/div[2]/div[1]"
                                                 + "/div/div/main/div/div[2]/div/header"
                                                 + "/div/div[2]/div/aui-dropdown-menu[1]"
                                                 + "/aui-section[6]/div/aui-item-link[2]/a",
                                                 )
            clone_btn.click()
            time.sleep(0.5)
        except TimeoutException as error:
            error = "An Error occured by clicking the clone button"
            print(error)
        try:
            create_btn = self.driver.find_element(
                By.XPATH,
                "/html/body/div[10]/div[2]/form/div[2]/div/input",
            )
            create_btn.click()
            self.driver.implicitly_wait(40)
        except TimeoutException as error:
            error = "An Error occured by clicking the create button"
            print(error)

    def set_issue_key(self):
        # get the name (issue_key) of the newly created ticket
        issue_key = self.driver.find_element (
                                             By.XPATH,
                                             "/html/body/div[1]/div[2]/div[1]"
                                             + "/div/div/main/div/div[2]/div/header"
                                             + "/div/div[1]/div/div[2]/ol/li[2]/a"
                                             )
        self.issue_key1 = issue_key.text
        return self.issue_key1

    def tearDown(self):
        # Browser schlie??en
        self.driver.quit()

def clone_run():
    cloneticket.setUp(cloneticket)
    cloneticket.test_runner(cloneticket)
    i_key = cloneticket.set_issue_key(cloneticket)
    cloneticket.tearDown(cloneticket)
    return i_key
