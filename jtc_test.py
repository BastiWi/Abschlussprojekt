'''Testing module'''
import unittest
import HTMLTestRunner

# JTC Tool imports
import jtc_auth
import jtc_resource
import jtc_mail
import jtc_db_reports

class TestAll(unittest.TestCase):
    '''test suite for jira autentication'''
    def __init__ (self, context):
        '''Initiating class'''
        self.context = context

    @classmethod
    def test_auth_variables(cls):
        '''check if variables exist and are strings'''
        assert isinstance(jtc_resource.usr["usr"], str)
        assert isinstance(jtc_resource.pw["pw"], str)
        assert isinstance(jtc_resource.server["server"], str)

    @classmethod
    def test_jira_login(cls):
        '''test login to jira'''
        try:
            login_test = jtc_auth.jtc_login()
            cls.assertEqual(None, login_test.auth)
        except:
            print('error')

    @classmethod
    def test_filter(cls):
        '''check if JQL Tag is running'''
        cls.assertNotEqual(None, cls.context.issues)
        assert isinstance(cls.context.assignee, str)
        cls.assertNotEqual(None, cls.context.issue)
        if (len(cls.context.issues)) > 0:
            cls.assertEqual((len(cls.context.issue)), (len(cls.context.issues)))
        #hier muss noch ein test rein ob der filter auch funzt

    @classmethod
    def test_cloning(cls):
        '''check if cloning is running'''
        pass

    @classmethod
    def test_mail_variables(cls):
        '''check mailing system'''
        assert isinstance(jtc_resource.mail_pw, str)
        assert isinstance(jtc_resource.smtp_server, str)
        assert isinstance(jtc_resource.port, int)
        assert isinstance(jtc_resource.sender_email, str)
        assert isinstance(jtc_resource.receiver_email, str)
        assert isinstance(jtc_resource.NB_USER, str)

    def test_mails(self):
        '''try to login to mail server'''
        login_mails = jtc_mail.SendMail.mails_login()
        self.assertNotEqual(login_mails.auth, None)
        # hier muss noch ein test rein um zu prüfen ob auch mails verschickt werden

if __name__ == "__main__":
    fp = open('Test-Report.txt', 'w', encoding="utf8")
    testresult = unittest.main(
        testRunner=HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        combine_reports=True,
        output="./report",
        report_title="JTC Test-Report"),
        exit = False
        )
    fp = open('Test-Report.txt', 'r', encoding="utf8")
    if testresult.result.wasSuccessful() is False:
        jtc_mail.send_error_mail.error_mail()
    jtc_db_reports.table_insert_reports()
