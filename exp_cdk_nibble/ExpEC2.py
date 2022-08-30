"""Building an EC2 instance for testing"""
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
)
from constructs import Construct


class ExpEC2(Stack):



    """EC2 instance construction"""
    def __init__(
            self, scope: Construct, construct_id: str, target_vpc, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        with open("./userdata/puppers.sh", encoding="utf-8") as file:
            user_data = file.read()

        ec2_optimized_ami = ecs.EcsOptimizedImage.amazon_linux2()
        role = iam.Role(
            self,
            "InstanceSSM",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )
        self.instance = ec2.Instance(
            self,
            "Instance",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ec2_optimized_ami,
            vpc=target_vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
            ),
            role=role,
            user_data=ec2.UserData.custom(user_data),
        )
