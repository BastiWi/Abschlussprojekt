'''Filter Project ASCCR to get the Tickets which should be blocked by Softwaretest Ticket'''
import jtc_auth
import jtc_clone
import jtc_resource
import mysql.connector
import sys


def jtc_issuefilter():
    # Run filter with original JQL TAG:
    # filter = 105117 AND NOT (issueFunction in linkedIssuesOf("issueFunction in linkedIssuesOf
    # (\"filter=105117\", \"depends on\") AND project = ASCSWTEST") AND project = ASCCR)
    # to find flagged tickets with the label [ENABLED_ASCSWTEST_AUTOLINKAGE]
    
    jira = jtc_auth.jtc_login()
    issues = []
    # for issue in jira.search_issues(
    #     "\u0066\u0069\u006c\u0074\u0065\u0072\u0020\u003d\u0020\u0031\u0030"
    #     + "\u0035\u0031\u0031\u0037\u0020\u0041\u004e\u0044\u0020\u004e\u004f"
    #     + "\u0054\u0020\u0028\u0069\u0073\u0073\u0075\u0065\u0046\u0075\u006e"
    #     + "\u0063\u0074\u0069\u006f\u006e\u0020\u0069\u006e\u0020\u006c\u0069"
    #     + "\u006e\u006b\u0065\u0064\u0049\u0073\u0073\u0075\u0065\u0073\u004f"
    #     + "\u0066\u0028\u0022\u0069\u0073\u0073\u0075\u0065\u0046\u0075\u006e"
    #     + "\u0063\u0074\u0069\u006f\u006e\u0020\u0069\u006e\u0020\u006c\u0069"
    #     + "\u006e\u006b\u0065\u0064\u0049\u0073\u0073\u0075\u0065\u0073\u004f"
    #     + "\u0066\u0028\u005c\u0022\u0066\u0069\u006c\u0074\u0065\u0072\u003d"
    #     + "\u0031\u0030\u0035\u0031\u0031\u0037\u005c\u0022\u002c\u0020\u005c"
    #     + "\u0022\u0064\u0065\u0070\u0065\u006e\u0064\u0073\u0020\u006f\u006e"
    #     + "\u005c\u0022\u0029\u0020\u0041\u004e\u0044\u0020\u0070\u0072\u006f"
    #     + "\u006a\u0065\u0063\u0074\u0020\u003d\u0020\u0041\u0053\u0043\u0053"
    #     + "\u0057\u0054\u0045\u0053\u0054\u0022\u0029\u0020\u0041\u004e\u0044"
    #     + "\u0020\u0070\u0072\u006f\u006a\u0065\u0063\u0074\u0020\u003d\u0020"
    #     + "\u0041\u0053\u0043\u0043\u0052\u0029"):
    #     issues.append(issue.key)
    # print(issues)

    for issue in jira.search_issues(
        "\u0070\u0072\u006f\u006a\u0065\u0063\u0074\u0020\u003d\u0020\u0041\u0053\u0043\u0043\u0052\u0020\u004f\u0052\u0044\u0045\u0052\u0020\u0042\u0059\u0020\u0052\u0061\u006e\u006b\u0020\u0041\u0053\u0043"):
        issues.append(issue.key)
    print(issues)

    # Run through all filtered Tickets, clone a Softwaretest Ticket,
    # set new assignee and block base Ticket by link
    issue = []
    assignee = jtc_resource.assignee["assignee"]
    for i in range(len(issues)):
        issuekey2 = jtc_clone.clone_run()
        issue.append(issuekey2)
        jira.assign_issue(issuekey2, assignee)
        jira.create_issue_link (
                               type="depends on",
                               inwardIssue=issues[i],
                               outwardIssue=issuekey2
                               )
    print(issue)

    for m in range(len(issue)): 
        try:
            conn = mysql.connector.connect(
                user="root",
                password="",
                host="127.0.0.1",
                port=3306,
                database="jtc_db"
            )
        except mysql.connector.Error as e:
            print(f"Error connecting to mySQL Platform: {e}")
            sys.exit(1)

            # Get Cursor
        cur = conn.cursor()
        sql = "INSERT INTO new_issues (issue, link) VALUES (%s, %s)"
        issue_link = "https://jira-test1.elektrobit.com/browse/"+issue[m]
        print("issue Link = "+issue_link)
        print(issue[m])
        val = (issue[m], issue_link)
        cur.execute(sql, val)
        conn.commit()

    return issue, issues, assignee

def run_jtc():
    # Create instance of filter()
    mail_info = jtc_issuefilter()
    return mail_info
