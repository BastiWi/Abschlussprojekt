'''main starting module'''
import jtc_mail
import jtc_prefilter
import jtc_filter
import jtc_context

def jtc_run():
    jtc_prefilter.jtc_prefiltering.jtc_run_prefilter()
    issue, issues, assignee = jtc_filter.jtc_issuefilter()
    context = jtc_context.jtc_context(issue, issues, assignee)   
    mails = jtc_mail.SendMail(context)
    mails.mail_content()

if __name__ =='__main__':
    jtc_run()
