from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class ExpCdkNibbleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = ec2.Vpc(self, "TheVPC",
                      cidr="10.0.0.0/16"
                      )
 = ec2.Vpc(self, "TheVPC",
                      cidr="10.0.0.0/16"