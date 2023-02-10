'''blubbl'''
from jira import __version__
from jira import JIRA
import jtc_resource
import jtc_clone

def jtc():
    '''Main program part to authenticate to jira, to filter the project,
    assign employees and block-link tickets'''

        # Authenticate to JIRA Project ASCCR with personal credentials

    jira = JIRA(server='https://jira-test1.elektrobit.com/',
                basic_auth=(jtc_resource.usr["usr"], jtc_resource.pw["pw"]))

        # Filter Project ASCCR to get the Tickets which should be blocked by Softwaretest Ticket

    issues = []
    # Original JQL TAG: [ASCCR] all approved (not closed) CRs depending on ASCSWTEST AND ASCSWTEST ticket NOT linked with the linked type "depends on"
    for issue in jira.search_issues(
        "\u0066\u0069\u006c\u0074\u0065\u0072\u0020\u003d\u0020\u0031\u0030\u0035\u0031\u0031\u0037\u0020\u0041\u004e\u0044\u0020\u004e\u004f\u0054\u0020\u0028\u0069\u0073\u0073\u0075\u0065\u0046\u0075\u006e\u0063\u0074\u0069\u006f\u006e\u0020\u0069\u006e\u0020\u006c\u0069\u006e\u006b\u0065\u0064\u0049\u0073\u0073\u0075\u0065\u0073\u004f\u0066\u0028\u0022\u0069\u0073\u0073\u0075\u0065\u0046\u0075\u006e\u0063\u0074\u0069\u006f\u006e\u0020\u0069\u006e\u0020\u006c\u0069\u006e\u006b\u0065\u0064\u0049\u0073\u0073\u0075\u0065\u0073\u004f\u0066\u0028\u005c\u0022\u0066\u0069\u006c\u0074\u0065\u0072\u003d\u0031\u0030\u0035\u0031\u0031\u0037\u005c\u0022\u002c\u0020\u005c\u0022\u0064\u0065\u0070\u0065\u006e\u0064\u0073\u0020\u006f\u006e\u005c\u0022\u0029\u0020\u0041\u004e\u0044\u0020\u0070\u0072\u006f\u006a\u0065\u0063\u0074\u0020\u003d\u0020\u0041\u0053\u0043\u0053\u0057\u0054\u0045\u0053\u0054\u0022\u0029\u0020\u0041\u004e\u0044\u0020\u0070\u0072\u006f\u006a\u0065\u0063\u0074\u0020\u003d\u0020\u0041\u0053\u0043\u0043\u0052\u0029",
        maxResults=50):
        issues.append(issue.key)
    print(issues)

        # Run through all filtered Tickets, clone a Softwaretest Ticket,
        # set new assignee and block base Ticket by link

    issue = []
    assignee = 'Sebastian Wicke'
    for i in range(len(issues)):
        issuekey2 = jtc_clone.clone_run()
        issue.append(issuekey2)
        jira.assign_issue(issuekey2, assignee)
        jira.create_issue_link( type="depends on", inwardIssue=issues[i], outwardIssue=issuekey2 )
    print(issue)
    return issue

def run_jtc():
    mail_info = jtc()
    return mail_info
