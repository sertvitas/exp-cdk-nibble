import aws_cdk as core
import aws_cdk.assertions as assertions

from exp_cdk_nibble.connectivity import ExpCdkNibbleStack

# example tests. To run these tests, uncomment this file along with the example
# resource in exp_cdk_nibble/connectivity.py
def test_sqs_queue_created():
    app = core.App()
    stack = ExpCdkNibbleStack(app, "exp-cdk-nibble")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
