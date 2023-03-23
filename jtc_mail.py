'''Module to send either "no Fail" e-mail or "error" e-mail'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jtc_resource

class SendMail:
    # creating mails
    def __init__ (self, context):
        self.context = context

    @classmethod
    def mails_login(self):
        # Try to log in to smtp server
        smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
        return smtp

    def mail_content(self):
        # create mail whether at least 1 ticket has been created or another when no 
        # ticket has been created
        if (len(self.context.issues)) > 0:
            smtp = self.mails_login()
            subject = "Report JTC - Automization TicketCreator"
            msg1 = f"""\
                Hi {self.context.assignee},\n\n
                These new Tickets have been created.\n
                \n
                {str(self.context.issue)}
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

        elif (len(self.context.issues)) == 0:
            smtp = self.mails_login()
            subject = "Report JTC - Automization TicketCreator"

            msg2 = f"""\
                Hi {self.context.assignee},\n\n
                No new Tickets have been created.\n
                \n
                Thank you and have a nice day!!!
                \n
                """
            msg = MIMEMultipart()
            msg.attach(MIMEText(msg2))
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

class send_error_mail:
    # def __init__(self):

    @classmethod
    def error_mail(self):
        # send testreport if errors occurred while testing
        smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
        subject = "Report JTC - Testing ErrorMessage"

        msg3 = f"""\
            Hi Sebastian,\n\n
            There have been Issues while running the Testing Suite.\n
            Please check the attachment for first information.\n
            \n
            For further information check the Testreports\n
            via the Links in the Database.\n
            \n
            Thank you and have a nice day!!!
            \n
            """
        msg = MIMEMultipart()
        msg.attach(MIMEText(msg3))
        file = open('Test-Report.txt')
        msg.attach(MIMEText(file.read()))
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


