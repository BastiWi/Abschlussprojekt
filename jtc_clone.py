'''Module for cloning Ticket: ASCSWTEST-49'''
from jira import JIRAError
import json
import jtc_auth

def clone_run():
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
    print(new_issue)


    # ID of the parent ticket to attach subtasks to
    parent_issue = new_issue
    project_key = parent_issue.fields.project.key
    parent_issue_key = parent_issue.key

    # create subtask
    subtask1 = jira.create_issue (
                                project=project_key,
                                priority = {'name': 'Major'},
                                summary='Support from virtual integration team for <feature>',
                                description='Description:\n'
                                            +'Work packages:\n'
                                                + '1. Kick off (1 or 2 hours): virtual integration team introduces software test development team to the feature\n'
                                                + '2. Verification criteria: create "feavc" specobjects according to Requirements management plan\n'
                                                + '3. Provide support with ECU configuration\n'
                                                + '4. Review test specification',
                                issuetype={'name': 'Sub-task'},
                                parent={'key': parent_issue_key}
                                )

    subtask2 = jira.create_issue (
                                project=project_key,
                                priority = {'name': 'Major'},
                                summary='Get familiar with the feature <feature>',
                                description='Description:\n'
                                            +'TBD\n'
                                                + 'Acceptance criteria:\n'
                                                + 'Understood the basic functionality of the feature\n',
                                issuetype={'name': 'Sub-task'},
                                parent={'key': parent_issue_key}
                                )

    subtask3 = jira.create_issue (
                                project=project_key,
                                priority = {'name': 'Major'},
                                summary='Create branch and remove it after merge to trunk for <feature>',
                                description='Description:\n'
                                            +'TBD\n'
                                                + 'Acceptance criteria:\n'
                                                + '1. Branch created\n'
                                                + '2. Merge To Trunk ticket closed\n'
                                                + '3. Branch deleted',
                                issuetype={'name': 'Sub-task'},
                                parent={'key': parent_issue_key}
                                )

    subtask4 = jira.create_issue (
                                project=project_key,
                                priority = {'name': 'Major'},
                                summary='Create Tricore configuration for <feature>',
                                description='Description:\n'
                                            +'TBD\n'
                                                + 'Acceptance criteria:\n'
                                                + '1. Configuration generated and build properly using the latest ACG delivered\n'
                                                + '2. Config files reviewed\n',
                                issuetype={'name': 'Sub-task'},
                                parent={'key': parent_issue_key}
                                )

    subtask5 = jira.create_issue (
                                project=project_key,
                                priority = {'name': 'Major'},
                                summary='Test specification for <feature>',
                                description='Description:\n'
                                            +'TBD\n'
                                                + 'Acceptance criteria:\n'
                                                + '1. Test Specifications available in SCTM\n'
                                                + '2. Review of Test Specification done\n'
                                                + '3. Test Specifications export file from SCTM attached to this ticket'
                                                + '4. Review of VC done',
                                issuetype={'name': 'Sub-task'},
                                parent={'key': parent_issue_key}
                                )

    subtask6 = jira.create_issue (
                                project=project_key,
                                priority = {'name': 'Major'},
                                summary='Implement tests for <feature>',
                                description='Description:\n'
                                            +'TBD\n'
                                            + 'Acceptance criteria:\n'
                                                + '1. The tests are linked to test spec from SCTM.\n'
                                                + '2. Tests executed successfully\n'
                                                + '3. PEP8 code style followed\n'
                                                + '4. Review of test implementation done',
                                issuetype={'name': 'Sub-task'},
                                parent={'key': parent_issue_key}
                                )

    subtask7 = jira.create_issue (
                                project=project_key,
                                priority = {'name': 'Major'},
                                summary='Merge branch to trunk for <feature>',
                                description='Description:\n'
                                            +'TBD\n'
                                                + 'Acceptance criteria:\n'
                                                + '1. Test suite executed successfully on SCTM with the latest ITA version\n'
                                                + '2. Review done\n',
                                issuetype={'name': 'Sub-task'},
                                parent={'key': parent_issue_key}
                                )
    return str(new_issue)
