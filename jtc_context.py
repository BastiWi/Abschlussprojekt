'''class to save variables'''

class jtc_context:
    '''saving variables to make them usable in other functions'''
    def __init__ (self, issue, issues, assignee):
        self.issue = issue
        self.issues = issues
        self.assignee = assignee
