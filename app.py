#!/usr/bin/env python3

import aws_cdk as cdk

from exp_cdk_nibble.connectivity import ExpCdkNibbleStack
from exp_cdk_nibble.rds import RdsStack
from exp_cdk_nibble.PuppersRdsStack import PuppersRdsStack
from exp_cdk_nibble.PuppersEc2 import PuppersEc2


#default_env = cdk.Environment(account=AWS_ACCOUNT_NUMBER, region=DEFAULT_REGION)


app = cdk.App()
network_stack = ExpCdkNibbleStack(app, "ExpCdkNibbleStack")
rds_stack = RdsStack(app, "RdsStack",network_stack.vpc)
rds_stack.add_dependency(network_stack)
PuppersRdsStack = PuppersRdsStack(app, "PuppersRdsStack",network_stack.vpc)
PuppersRdsStack.add_dependency(network_stack)
PuppersEc2 = PuppersEc2(app, "PuppersEc2",network_stack.vpc, PuppersRdsStack.my_secret)
PuppersEc2.add_dependency(network_stack)
app.synth()
