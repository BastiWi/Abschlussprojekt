'''main starting module'''
import jtc_mail
import jtc_prefilter
# import jtc_testing_suite

def jtc_run():
    jtc_prefilter.jtc_prefilter.jtc_run_prefilter()
    # jtc_testing_suite.JTC_Test_Suite()
    jtc_mail.mailsender()

if __name__ =='__main__':
    jtc_run()
