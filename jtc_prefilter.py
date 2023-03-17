'''Filter Project ASCCR to get the Tickets which should be blocked by Softwaretest Ticket'''
import jtc_auth
import jtc_resource
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class jtc_prefilter:
    def jtc_run_prefilter():
        # Run filter with original JQL TAG:
        # filter = 105117 AND NOT (issueFunction in linkedIssuesOf("issueFunction in linkedIssuesOf
        # (\"filter=105117\", \"depends on\") AND project = ASCSWTEST") AND project = ASCCR)
        # to find ready-to-be-flagged tickets
        
        jira = jtc_auth.jtc_login()
        prefiltered_issues = []
        for issue in jira.search_issues(
            "\u0066\u0069\u006c\u0074\u0065\u0072\u0020\u003d\u0020\u0031\u0030"
            + "\u0035\u0031\u0031\u0037\u0020\u0041\u004e\u0044\u0020\u004e\u004f"
            + "\u0054\u0020\u0028\u0069\u0073\u0073\u0075\u0065\u0046\u0075\u006e"
            + "\u0063\u0074\u0069\u006f\u006e\u0020\u0069\u006e\u0020\u006c\u0069"
            + "\u006e\u006b\u0065\u0064\u0049\u0073\u0073\u0075\u0065\u0073\u004f"
            + "\u0066\u0028\u0022\u0069\u0073\u0073\u0075\u0065\u0046\u0075\u006e"
            + "\u0063\u0074\u0069\u006f\u006e\u0020\u0069\u006e\u0020\u006c\u0069"
            + "\u006e\u006b\u0065\u0064\u0049\u0073\u0073\u0075\u0065\u0073\u004f"
            + "\u0066\u0028\u005c\u0022\u0066\u0069\u006c\u0074\u0065\u0072\u003d"
            + "\u0031\u0030\u0035\u0031\u0031\u0037\u005c\u0022\u002c\u0020\u005c"
            + "\u0022\u0064\u0065\u0070\u0065\u006e\u0064\u0073\u0020\u006f\u006e"
            + "\u005c\u0022\u0029\u0020\u0041\u004e\u0044\u0020\u0070\u0072\u006f"
            + "\u006a\u0065\u0063\u0074\u0020\u003d\u0020\u0041\u0053\u0043\u0053"
            + "\u0057\u0054\u0045\u0053\u0054\u0022\u0029\u0020\u0041\u004e\u0044"
            + "\u0020\u0070\u0072\u006f\u006a\u0065\u0063\u0074\u0020\u003d\u0020"
            + "\u0041\u0053\u0043\u0043\u0052\u0029"):
            prefiltered_issues.append(issue.key)
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
            # create mail whether at least 1 ticket has been found to be flagged
            if (len(prefiltered_issues)) > 0:
                smtp = smtplib.SMTP("mail-de.ebgroup.elektrobit.com", 587)
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(jtc_resource.NB_USER, jtc_resource.mail_pw)
                subject = "Report JTC - Automization"
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
                                msg.as_string()
                                )
                except smtplib.SMTPSenderRefused as error:
                    print(error)
                smtp.close()
        
        mails_login_prefilter()
        mail_content_prefilter()
