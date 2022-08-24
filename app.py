#!/usr/bin/env python3

import aws_cdk as cdk

from exp_cdk_nibble.connectivity import ExpCdkNibbleStack
from exp_cdk_nibble.rds import RdsStack
from exp_cdk_nibble.rds_11 import Rds11Stack

#default_env = cdk.Environment(account=AWS_ACCOUNT_NUMBER, region=DEFAULT_REGION)


app = cdk.App()
network_stack = ExpCdkNibbleStack(app, "ExpCdkNibbleStack")
rds_stack = RdsStack(app, "RdsStack",network_stack.vpc)
rds_stack.add_dependency(network_stack)
rds11_stack = Rds11Stack(app, "Rds11Stack",network_stack.vpc)
rds11_stack.add_dependency(network_stack)
app.synth()
