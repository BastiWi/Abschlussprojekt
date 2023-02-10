'''blubbl'''
import smtplib
import ssl
import jtc_start
import jtc_resource
from email import mime

SMTP_SERVER = "mail-de.ebgroup.elektrobit.com"
PORT = 587
SENDER_EMAIL = "JTC-update-mail"

inform_me = jtc_start.run_jtc()

def send_mail():
    '''send a mail when alt least 1 ticket has been created else send a mail when no ticket has been created'''
    # Try to log in to server and send email
    if (len(inform_me)) > 0:
        # Try to log in to server and send email
        smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(jtc_resource.sender_email("sender"), jtc_resource.mail_pw("mail_pw"))
        msg1 = """\
                Subject: Report JTC - Automization
                Hi {assignee},\n\n
                These new Tickets have been created:\n
                {issue}\n"""
        smtp.sendmail(jtc_resource.sender_email("sender"), jtc_resource.receiver_email("receiver"), msg1)
        smtp.close()
        

    else:
        # Try to log in to server and send email
        smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
        msg2 = """\
                Subject: Report JTC - Automization
                Hi {assignee},\n\n
                No new Tickets have been created.\n
                """
        smtp.sendmail(jtc_resource.sender_email, jtc_resource.receiver_email, msg2)
        smtp.close()

send_mail()
