'''program part to login to jira'''
from jira import __version__
from jira import JIRA
import jtc_resource

def jtc_login():
    '''Authenticate to JIRA Project ASCCR with personal credentials'''
    jira = JIRA(server=jtc_resource.server["server"],
                basic_auth=(jtc_resource.usr["usr"], jtc_resource.pw["pw"]))
    return jira
