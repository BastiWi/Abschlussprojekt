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
import jtc_mail
import jtc_db_reports

class TestAll(unittest.TestCase):
    def __init__ (self, context):
        self.context = context
    # test suite for jira autentication
    @classmethod
    def test_auth_variables(self):
        #check if variables exist and are strings
        assert isinstance(jtc_resource.usr["usr"], str)
        assert isinstance(jtc_resource.pw["pw"], str)
        assert isinstance(jtc_resource.server["server"], str)
    @classmethod
    def test_jira_login(self):
        # test login to jira
        try:
            login_test = jtc_auth.jtc_login()
            self.assertEqual(None, login_test.auth)
        except:
            print('error')
    @classmethod
    def test_filter(self):
        # check if JQL Tag is running
        self.assertNotEqual(None, self.context.issues)
        assert isinstance(self.context.assignee, str)
        self.assertNotEqual(None, self.context.issue)
        if (len(self.context.issues)) > 0:
            self.assertEqual((len(self.context.issue)), (len(self.context.issues)))
#hier muss noch ein test rein ob der filter auch funzt
   
    @classmethod
    def test_cloning(self):
        

    @classmethod
    def test_mail_variables(self):
        # check mailing system
        assert isinstance(jtc_resource.mail_pw, str)
        assert isinstance(jtc_resource.smtp_server, str)
        assert isinstance(jtc_resource.port, int)
        assert isinstance(jtc_resource.sender_email, str)
        assert isinstance(jtc_resource.receiver_email, str)
        assert isinstance(jtc_resource.NB_USER, str)

    def test_mails(self):
        # try to login to mail server
        login_mails = jtc_mail.SendMail.mails_login()
        self.assertNotEqual(login_mails.auth, None)
        # hier muss noch ein test rein um zu prüfen ob auch mails verschickt werden    


if __name__ == "__main__":
    fp = open('Test-Report.txt', 'w')
    testresult = unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(stream=fp, combine_reports=True, output="./report", report_title="JTC Test-Report"), exit = False)
    fp = open('Test-Report.txt', 'r')
    if testresult.result.wasSuccessful() == False:
        jtc_mail.send_error_mail.error_mail()
    jtc_db_reports.table_insert_reports()
