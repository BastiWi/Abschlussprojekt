'''blubbl'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import jtc_filter
import jtc_resource

issue, issues, assignee = jtc_filter.run_jtc()

class SendMail():
    '''creating mails:'''
    def mails_login():
        '''Try to log in to smtp server'''
        smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
        return smtp

    def mail_content():
        '''create mail whether at least 1 ticket has been created or another when no 
        ticket has been created or send testreport if errors occurred while testing'''
        if (len(issues)) > 0:
            smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
            subject = "Report JTC - Automization"
            msg1 = f"""\
                Hi {assignee},\n\n
                These new Tickets have been created.\n
                No Issues occurred while testing.\n
                \n
                {str(issue)}
                \n
                Thank you and have a nice day!!!
                """
            msg = MIMEMultipart()
            msg.attach(MIMEText(msg1))
            file = open('Test-Report.txt')
            msg.attach(MIMEText(file.read()))
            msg['Subject'] = subject
            msg['To'] = jtc_resource.receiver_email
            try:
                smtp.sendmail(jtc_resource.sender_email,
                    jtc_resource.receiver_email, msg.as_string())
            except smtplib.SMTPSenderRefused as error:
                print(error)
            smtp.close()

        elif (len(issues)) == 0:
            smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
            subject = "Report JTC - Automization"

            msg2 = f"""\
                Hi {assignee},\n\n
                No new Tickets have been created.\n
                No Issues occurred while testing.\n
                \n
                Thank you and have a nice day!!!
                \n
                """
            msg = MIMEMultipart()
            msg.attach(MIMEText(msg2))
            file = open('Test-Report.txt')
            msg.attach(MIMEText(file.read()))
            msg['Subject'] = subject
            msg['To'] = jtc_resource.receiver_email
            try:
                smtp.sendmail(jtc_resource.sender_email,
                    jtc_resource.receiver_email, msg.as_string())
            except smtplib.SMTPSenderRefused as error:
                print(error)
            smtp.close()

class send_error_mail():
    def error_mail():
        smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
        subject = "Report JTC - Automization"

        msg3 = f"""\
            Hi {assignee},\n\n
            There have been Issues while running the Testing Suite.\n
            Please check the attachment for first information.\n
            For further information check the Database Testreports.\n
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
            smtp.sendmail(jtc_resource.sender_email,
                jtc_resource.receiver_email, msg.as_string())
        except smtplib.SMTPSenderRefused as error:
            print(error)
        smtp.close()


def mailsender():
    '''send Mail and close server'''
    SendMail.mail_content()
