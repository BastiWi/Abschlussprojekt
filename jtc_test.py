'''Testing module'''
import unittest
import time
import HTMLTestRunner

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# JTC Tool imports
import jtc_auth
import jtc_resource
import jtc_filter
import jtc_mail
import jtc_db_reports
import jtc_context

class TestAll(unittest.TestCase):
    # test suite for jira autentication
    def test_auth_variables(self):
        #check if variables exist and are strings
        assert isinstance(jtc_resource.usr["usr"], str)
        assert isinstance(jtc_resource.pw["pw"], str)
        assert isinstance(jtc_resource.server["server"], str)

    # def test_jira_login(self):
    #     # test login to jira
    #     try:
    #         login_test = jtc_auth.jtc_login()
    #         self.assertEqual(None, login_test.auth)
    #     except:
    #         print('error')

    def test_filter(self):
        # check if JQL Tag is running
        issues, issue, assignee = jtc_filter.jtc_issuefilter()
        self.assertNotEqual(None, issues)
        assert isinstance(assignee, str)
        self.assertNotEqual(None, issue)
        if (len(issues)) > 0:
            self.assertEqual((len(issue)), (len(issues)))
#hier muss noch ein test rein ob der filter auch funzt

    def setUp(self):
        # test suite for cloning tickets with selenium
        # setup selenium frame
        issue, issues, assignee = jtc_filter.run_jtc()
        self.context = jtc_context(issue, issues, assignee)
        self.mail = jtc_mail.SendMail(self.context)
        self.baseUrl = "https://jira-test1.elektrobit.com/browse/ASCSWTEST-49"
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(0.2)
        self.driver.get(self.baseUrl)

    def test_clone(self):
        # check if cloning works
        self.baseUrl = "https://jira-test1.elektrobit.com/browse/ASCSWTEST-49"
        self.driver.get(self.baseUrl)
        usr = jtc_resource.usr["usr"]
        password = jtc_resource.pw["pw"]
        try:
            usr_input = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div/main/form/div[1]/div[2]/div/div[1]/input",
            )
            usr_input.send_keys(usr)
            time.sleep(0.5)
        except TimeoutException as error:
            error = "An Error occured at sending username"
            print(error)
        try:
            pw_input = self.driver.find_element (
                By.XPATH,
                "/html/body/div/div/div/div/main/form/div[1]/div[2]/div/div[2]/input",
                )
            pw_input.send_keys(password)
            time.sleep(0.5)
        except TimeoutException as error:
            error = "An Error occured at sending password"
            print(error)
        try:
            login_btn = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div/main/form/div[2]/div/input",
            )
            login_btn.click()
            time.sleep(0.5)
            self.assertIn("EB external Jira",self.driver.title)
        except TimeoutException as error:
            error = "An Error occured by clicking the login button"
            print(error)
        try:
            more_btn = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[1]/div/div/main/div/div[2]/div"+
                "/header/div/div[2]/div/div/div/div[1]/div[3]/a[2]/span",
            )
            more_btn.click()
            time.sleep(0.5)
        except TimeoutException as error:
            error = "An Error occured by clicking the more button"
            print(error)
        try:
            clone_btn = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[1]/div/div/main/div/div[2]/div/header"+
                "/div/div[2]/div/aui-dropdown-menu[1]/aui-section[6]/div/aui-item-link[2]/a",
            )
            clone_btn.click()
            time.sleep(0.5)
        except TimeoutException as error:
            error = "An Error occured by clicking the clone button"
            print(error)

    def set_issue_key(self):
        # try to get issue key
        try:
            self.driver.find_element(By.XPATH,
            "/html/body/div[1]/div[2]/div[1]/div/div/main/div/div[2]/div/header"+
            "/div/div[1]/div/div[2]/ol/li[2]/a")
        except TimeoutException as error:
            error = "Issue Key could not be found"
            print(error)

    def tearDown(self):
        # close browser
        self.driver.quit()

    def test_mail_variables(self):
        # check mailing system
        assert isinstance(jtc_resource.mail_pw, str)
        assert isinstance(jtc_resource.smtp_server, str)
        assert isinstance(jtc_resource.port, int)
        assert isinstance(jtc_resource.sender_email, str)
        assert isinstance(jtc_resource.receiver_email, str)
        assert isinstance(jtc_resource.NB_USER, str)

    #def test_mails(self):
        # try to login to mail server
    #     login_mails = jtc_mail.SendMail.mails_login()
    #     self.assertNotEqual(login_mails.auth, None)
        # hier muss noch ein test rein um zu prüfen ob auch mails verschickt werden    


if __name__ == "__main__":
    fp = open('Test-Report.txt', 'w')
    testresult = unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(stream=fp, combine_reports=True, output="./report", report_title="JTC Test-Report"), exit = False)
    fp = open('Test-Report.txt', 'r')
    if testresult.result.wasSuccessful() == False:
        jtc_mail.send_error_mail.error_mail()
    jtc_db_reports.table_insert_reports()
