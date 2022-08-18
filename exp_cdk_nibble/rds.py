import json
from aws_cdk import (
    Stack,
    aws_secretsmanager as sm,
    aws_rds as rds,
    aws_ec2 as ec2,
)
from constructs import Construct


class RdsStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, target_vpc, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        my_secret = sm.Secret(
            self,
            "Secret",
            generate_secret_string=sm.SecretStringGenerator(
                secret_string_template=json.dumps(
                    {"username": "postgres"}, separators=(",", ":")
                ),
                generate_string_key="password",
                exclude_punctuation=True
            ),
        )
        instance1 = rds.DatabaseInstance(
            self,
            "PostgresInstance1",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            credentials=rds.Credentials.from_secret(my_secret),
            vpc=target_vpc,
            allocated_storage=100,
            allow_major_version_upgrade=False,
            auto_minor_version_upgrade=False,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.SMALL
            ),
            # backup_retention=,
            copy_tags_to_snapshot=True,
            deletion_protection=False,
            enable_performance_insights=True,
            multi_az=True,
            # parameter_group=,
            # preferred_backup_window=,
            # preferred_maintenance_window=,
            # removal_policy=,
            # storage_type=,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )
        sm.SecretRotation(
            self,
            "SecretRotation",
            application=sm.SecretRotationApplication.POSTGRES_ROTATION_SINGLE_USER,
            # Postgres single user scheme
            secret=my_secret,
            target=instance1,  # a Connectable
            vpc=target_vpc,  # The VPC where the secret rotation application will be deployed
            exclude_characters=" %+:;\{\}'\"\,@\\",
        )
