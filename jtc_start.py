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
    # Original JQL TAG: description ~ "\"YES{color}* *Jira-Epic/s*
    # for each affected ART\""
    # AND NOT (description ~ "\"{color:#00875a}YES{color}* /
    # *{color:#de350b}NO{color}* *Jira-Epic/s*
    # for each affected ART\"")
    for issue in jira.search_issues(
        "\u0064\u0065\u0073\u0063\u0072\u0069\u0070\u0074\u0069\u006f\u006e\u0020\u007e\u0020\u0022\u005c\u0022\u0059\u0045\u0053\u007b\u0063\u006f\u006c\u006f\u0072\u007d\u002a\u0020\u002a\u004a\u0069\u0072\u0061\u002d\u0045\u0070\u0069\u0063\u002f\u0073\u002a\u0020\u0066\u006f\u0072\u0020\u0065\u0061\u0063\u0068\u0020\u0061\u0066\u0066\u0065\u0063\u0074\u0065\u0064\u0020\u0041\u0052\u0054\u005c\u0022\u0022\u0020\u0041\u004e\u0044\u0020\u004e\u004f\u0054\u0020\u0028\u0064\u0065\u0073\u0063\u0072\u0069\u0070\u0074\u0069\u006f\u006e\u0020\u007e\u0020\u0022\u005c\u0022\u007b\u0063\u006f\u006c\u006f\u0072\u003a\u0023\u0030\u0030\u0038\u0037\u0035\u0061\u007d\u0059\u0045\u0053\u007b\u0063\u006f\u006c\u006f\u0072\u007d\u002a\u0020\u002f\u0020\u002a\u007b\u0063\u006f\u006c\u006f\u0072\u003a\u0023\u0064\u0065\u0033\u0035\u0030\u0062\u007d\u004e\u004f\u007b\u0063\u006f\u006c\u006f\u0072\u007d\u002a\u0020\u002a\u004a\u0069\u0072\u0061\u002d\u0045\u0070\u0069\u0063\u002f\u0073\u002a\u0020\u0066\u006f\u0072\u0020\u0065\u0061\u0063\u0068\u0020\u0061\u0066\u0066\u0065\u0063\u0074\u0065\u0064\u0020\u0041\u0052\u0054\u005c\u0022\u0022\u0029",
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
