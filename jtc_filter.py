'''Filter Project ASCCR to get the Tickets which should be blocked by Softwaretest Ticket'''
import sys
import mysql.connector
import jtc_auth
import jtc_clone
import jtc_resource

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

def jtc_issuefilter():
    '''Run filter to find flagged tickets with the label [ENABLED_ASCSWTEST_AUTOLINKAGE]'''

    jira = jtc_auth.jtc_login()
    myfilter = 'filter = 105250 AND (labels = ENABLED_ASCSWTEST_AUTOLINKAGE)'
    encoded_filter = myfilter.encode("utf-8")
    issues = []
    for issue in jira.search_issues(encoded_filter):
        issues.append(issue.key)
    print(issues)

    # Run through all filtered Tickets, clone a Softwaretest Ticket,
    # set new assignee and block base Ticket by link
    jira = jtc_auth.jtc_login()
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
        if i == 1:
            break
    print(issue)

    for m in range(len(issue)):
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
