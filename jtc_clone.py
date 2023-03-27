'''Module for cloning Ticket: ASCSWTEST-49'''
import json
from jira import JIRAError
import jtc_auth

def clone_run():
    '''Class to run the cloning of tickets'''
    jira = jtc_auth.jtc_login()

    def create_jira_issue(jira, fields, retries=3):
        """
        Creates a Jira issue with given fields. If fields are not allowed to be
        set, they are removed. By default it tries to create the issue three times.
        Returns Jira object and a list of removed fields.
        """
        try:
            new_issue = jira.create_issue(fields=fields, prefetch=True)
            return new_issue, []
        except JIRAError as e:
            if retries <= 0:
                raise e
            ignored_fields = []
            message = json.loads(e.response.text)
            for i in message['errors'].keys():
                if i in fields:
                    del fields[i]
                    ignored_fields.append(i)
            new_issue, b = create_jira_issue(jira, fields, retries-1)
            ignored_fields += b
            return new_issue, ignored_fields

    def clone_jira_issue(jira, origin_issue):
        """
        Clones the give Jira issue. Jira issue can be referenced by ID or
        by issue object.
        Returns Jira object and a list of removed fields.
        """
        if type(origin_issue) == str:
            origin_issue = jira.issue(origin_issue)

        fields = origin_issue.raw['fields']
        return create_jira_issue(jira, fields)

    new_issue, ignored_fields = clone_jira_issue(jira, 'ASCSWTEST-49')

    # ID of the parent ticket to attach subtasks to
    parent_issue = new_issue
    project_key = parent_issue.fields.project.key
    parent_issue_key = parent_issue.key

    # create subtask
    jira.create_issue (
                    project=project_key,
                    priority = {'name': 'Major'},
                    assignee = {'name': ''},
                    summary='Support from virtual integration team for <feature>',
                    description='*Description:*\n'
                        +'Work packages:\n'
                        + '# Kick off (1 or 2 hours):'
                        + 'virtual integration team introduces'
                        + 'software test development team to the feature\n'
                        + '# Verification criteria: create "feavc" specobjects according to'
                        + '[Requirements management plan|https://subversion.ebgroup.elektrobit.com'
                        + '/svn/autosar/asc_Project/trunk/doc/project/management/strategy/'
                        + 'Requirements_management_plan.docx]\n'
                        + '# Provide support with ECU configuration\n'
                        + '# Review test specification',
                    issuetype={'name': 'Sub-task'},
                    parent={'key': parent_issue_key}
                    )

    jira.create_issue (
                    project=project_key,
                    priority = {'name': 'Major'},
                    assignee = {'name': ''},
                    summary='Get familiar with the feature <feature>',
                    description='*Description:*\n\n'
                        +'TBD\n\n'
                        + '*Acceptance criteria:*\n'
                        + '  * Understood the basic functionality'
                        + ' of the feature\n',
                    issuetype={'name': 'Sub-task'},
                    parent={'key': parent_issue_key}
                    )

    jira.create_issue (
                    project=project_key,
                    priority = {'name': 'Major'},
                    assignee = {'name': ''},
                    summary='Create branch and remove it after'
                            + ' merge to trunk for <feature>',
                    description='*Description:*\n\n'
                        +'TBD\n\n'
                        + '*Acceptance criteria:*\n'
                        + '  * Branch created\n'
                        + '  * Merge To Trunk ticket closed\n'
                        + '  * Branch deleted',
                    issuetype={'name': 'Sub-task'},
                    parent={'key': parent_issue_key}
                    )

    jira.create_issue (
                    project=project_key,
                    priority = {'name': 'Major'},
                    assignee = {'name': ''},
                    summary='Create Tricore configuration for <feature>',
                    description='*Description:*\n\n'
                        +'TBD\n\n'
                        + '*Acceptance criteria:*\n'
                        + '  * Configuration generated and build'
                        + ' properly using the latest ACG delivered\n'
                        + '  * Config files reviewed\n',
                    issuetype={'name': 'Sub-task'},
                    parent={'key': parent_issue_key}
                    )

    jira.create_issue (
                    project=project_key,
                    priority = {'name': 'Major'},
                    assignee = {'name': ''},
                    summary='Test specification for <feature>',
                    description='*Description:*\n\n'
                        +'TBD\n\n'
                        + '*Acceptance criteria:*\n'
                        + '  * Test Specifications available in SCTM\n'
                        + '  * Review of Test Specification done\n'
                        + '  * Test Specifications export file'
                        + ' from SCTM attached to this ticket'
                        + '  * Review of VC done',
                    issuetype={'name': 'Sub-task'},
                    parent={'key': parent_issue_key}
                    )

    jira.create_issue (
                    project=project_key,
                    priority = {'name': 'Major'},
                    assignee = {'name': ''},
                    summary='Implement tests for <feature>',
                    description='*Description:*\n\n'
                        +'TBD\n\n'
                        + '*Acceptance criteria:*\n'
                        + '  * The tests are linked to'
                        + ' test spec from SCTM.\n'
                        + '  * Tests executed successfully\n'
                        + '  * PEP8 code style followed\n'
                        + '  * Review of test implementation done',
                    issuetype={'name': 'Sub-task'},
                    parent={'key': parent_issue_key}
                    )

    jira.create_issue (
                    project=project_key,
                    priority = {'name': 'Major'},
                    assignee = {'name': ''},
                    summary='Merge branch to trunk for <feature>',
                    description='*Description:*\n\n'
                        +'TBD\n\n'
                        + '*Acceptance criteria:*\n'
                        + '  * Test suite executed successfully'
                        + ' on SCTM with the latest ITA version\n'
                        + '  * Review done\n',
                    issuetype={'name': 'Sub-task'},
                    parent={'key': parent_issue_key}
                    )
    return str(new_issue)
