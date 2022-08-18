from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
)
from constructs import Construct


class ExpCdkNibbleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = ec2.Vpc(
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

        self.vpc.add_interface_endpoint(
            "EC2", service=ec2.InterfaceVpcEndpointAwsService.EC2
        )
        self.vpc.add_interface_endpoint(
            "EC2_MESSAGES",
            service=ec2.InterfaceVpcEndpointAwsService.EC2_MESSAGES,
        )
        self.vpc.add_interface_endpoint(
            "SSM", service=ec2.InterfaceVpcEndpointAwsService.SSM
        )
        self.vpc.add_interface_endpoint(
            "SSM_MESSAGES",
            service=ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES,
        )
        # vpc.add_interface_endpoint(
        #     "S3", service=ec2.InterfaceVpcEndpointAwsService.S3
        # )

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
        instance = ec2.Instance(
            self,
            "Instance",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ec2_optimized_ami,
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            role=role,
        )
