'''blubbl'''
import smtplib
import ssl
import jtc_start
import jtc_resource

SMTP_SERVER = "localhost"
PORT = 1025
SENDER_EMAIL = "localhost"

inform_me = jtc_start.run_jtc()

def send_mail():
    '''send a mail when alt least 1 ticket has been created else send a mail when no ticket has been created'''
    # Try to log in to server and send email
    if (len(inform_me)) > 0:
        # Create a secure SSL context
        context = ssl.create_default_context()
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(jtc_resource.smtp_server["smtp"], jtc_resource.port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(jtc_resource.sender_email["sender"], jtc_resource.pw["pw"])
            message = """\
                Subject: Report JTC - Automization
                Hi {assignee},\n\n
                The following new Tickets have been created:\n
                {issue}\n"""

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(jtc_resource.smtp_server["smtp"],
                                jtc_resource.port, context=context) as server:
                server.login(jtc_resource.sender_email["sender"], jtc_resource.pw["pw"])
                server.sendmail(jtc_resource.sender_email["sender"],
                                jtc_resource.receiver_email["receiver"], message)
        except Exception as exception:
            exception = "Oder auch nicht"
            print(exception)
        finally:
            server.quit()

    else:
        '''send a mail when no ticket has been created'''
        # Create a secure SSL context
        context = ssl.create_default_context()
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(jtc_resource.smtp_server["smtp"], jtc_resource.port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(jtc_resource.sender_email["sender"], jtc_resource.pw["pw"])
            message = """\
                Subject: Report JTC - Automization
                Hi {assignee},\n\n
                No new Tickets have been created.\n
                {issue}\n"""

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(jtc_resource.smtp_server["smtp"],
                                jtc_resource.port, context=context) as server:
                server.login(jtc_resource.sender_email["sender"], jtc_resource.pw["pw"])
                server.sendmail(jtc_resource.sender_email["sender"],
                                jtc_resource.receiver_email["receiver"], message)
        except Exception as exception:
            exception = "Oder auch nicht"
            print(exception)
        finally:
            server.quit()

send_mail()
