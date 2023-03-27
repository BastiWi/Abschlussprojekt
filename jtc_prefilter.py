'''Filter Project ASCCR to get the Tickets which should be blocked by Softwaretest Ticket'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jtc_auth
import jtc_resource

class jtc_prefiltering:
    '''Class for prefiltering the project ASCCR jira tickets'''
    def __init__(self, smtp):
        self.smtp = smtp

    @classmethod
    def jtc_run_prefilter(cls):
        '''Run filter to find ready-to-be-flagged tickets'''

        jira = jtc_auth.jtc_login()
        myfilter = 'filter = 105250 AND NOT (labels = ENABLED_ASCSWTEST_AUTOLINKAGE)'
        encoded_filter = myfilter.encode("utf-8")
        prefiltered_issues = []
        for prefiltered_issue in jira.search_issues(encoded_filter):
            prefiltered_issues.append(prefiltered_issue.key)
        print(prefiltered_issues)

        def mails_login_prefilter():
            # Try to log in to smtp server
            smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
            return smtp

        def mail_content_prefilter():
            '''create mail whether at least 1 ticket has been found to be flagged'''
            if (len(prefiltered_issues)) > 0:
                smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
                subject = "Report JTC - Automization PreFilter"
                msg1 = f"""\
                    Hi Gürkan,\n\n
                    These new Tickets will need to be flagged as \n
                    [ENABLED_ASCSWTEST_AUTOLINKAGE].\n
                    \n
                    {str(prefiltered_issues)}
                    \n
                    Thank you and have a nice day!!!
                    """
                msg = MIMEMultipart()
                msg.attach(MIMEText(msg1))
                msg['Subject'] = subject
                msg['To'] = jtc_resource.receiver_email
                try:
                    smtp.sendmail (
                                jtc_resource.sender_email,
                                jtc_resource.receiver_email,
                                msg.as_string()
                                )
                except smtplib.SMTPSenderRefused as error:
                    print(error)
                smtp.close()

        mails_login_prefilter()
        mail_content_prefilter()
