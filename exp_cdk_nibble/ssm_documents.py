""" Deploy SSM Documents
"""
import json
from aws_cdk import Stack, aws_ssm as ssm, CfnTag
from constructs import Construct


def get_content(template, shell_script):
    """The content is a JSON string that describes the SSM Document
    The shell script has to be chopped up into lines, convertes to a list and
    embedded in the JSON template.  This function assumes the SSM Document has
    only one action.

    Args:
        template (str): relative path to json template. example:
            ./resource/ssm/scripts/update_splunk.json
        shell_script (str): relative path to shell script. example:
            ./resource/ssm/scripts/update_splunk.sh
    """

    with open(shell_script, encoding="utf-8") as script_file:
        script_data = script_file.read()
        json_lines = script_data.splitlines()

    with open(template, encoding="utf-8") as json_file:
        content = json.load(json_file)
    content["mainSteps"][0]["inputs"]["runCommand"] = json_lines
    return content


class SsmDocumentsStack(Stack):
    """Stack deploys SSM Documents

    Args:
        Stack (_type_): _description_
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cfn_document = ssm.CfnDocument(
            self,
            "MyCfnDocument",
            content=get_content(
                "./resource/ssm/scripts/update_splunk.json",
                "./resource/ssm/scripts/update_splunk.sh",
            ),
            document_format="JSON",
            document_type="Command",
            name="zzzname",
            tags=[CfnTag(key="key", value="value")],
            target_type="/AWS::EC2::Instance",
            update_method="NewVersion",
        )
