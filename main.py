'''main starting module'''
import jtc_mail
import jtc_prefilter
import jtc_filter
import jtc_context
import jtc_testing_suite

def jtc_run():
    jtc_prefilter.jtc_prefiltering.jtc_run_prefilter()
    issue, issues, assignee = jtc_filter.run_jtc()
    context = jtc_context.jtc_context(issue, issues, assignee)
    jtc_testing_suite.JTC_Test_Suite(context)    
    mails = jtc_mail.SendMail(context)
    mails.mail_content()

if __name__ =='__main__':
    jtc_run()
