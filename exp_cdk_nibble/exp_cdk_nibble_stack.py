from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class ExpCdkNibbleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = ec2.Vpc(
            self,
            "TheVPC",
            cidr="10.0.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="nibble_public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name="nibble_private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                ),
                ec2.SubnetConfiguration(
                    name="nibble_isolated",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                ),
            ],
        )
