"""Creating and RDS stack on Postgres11 for upgrade testing"""
import json
from aws_cdk import (
    Stack,
    aws_secretsmanager as sm,
    aws_rds as rds,
    aws_ec2 as ec2,
)
from constructs import Construct


class PuppersRdsStack(Stack):
    """Constructing the stack"""

    def __init__(
        self, scope: Construct, construct_id: str, target_vpc, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.my_secret = sm.Secret(
            self,
            "Secret",
            generate_secret_string=sm.SecretStringGenerator(
                secret_string_template=json.dumps(
                    {"username": "postgres"}, separators=(",", ":")
                ),
                generate_string_key="password",
                exclude_punctuation=True,
            ),
        )
        # This command uses version checking against a table of "valid" versions.
        # engine = rds.DatabaseInstanceEngine.postgres(
        #    version=rds.PostgresEngineVersion.VER_11_13
        # )

        # PostgresEngineVersion.of allows arbitrary versions without validity checking.
        # Requires ('<full_version>','<major_version>')
        engine = rds.DatabaseInstanceEngine.postgres(
            version=rds.PostgresEngineVersion.of("11.13", "11")
        )
        parameter_group = rds.ParameterGroup(
            self,
            "ParameterGroup",
            engine=engine,
            parameters={
                "rds.logical_replication": "1",
                "autovacuum_naptime": "40",
                # rds.allowed_extensions requires ver 12.6+ only.
                # rds.allowed_extensions": "dblink, hstore, pg_stat_statements",
                "wal_sender_timeout": "0",
                "shared_preload_libraries": "pg_stat_statements",
            },
        )
        instance1 = rds.DatabaseInstance(
            self,
            "PostgresInstance1",
            engine=engine,
            parameter_group=parameter_group,
            credentials=rds.Credentials.from_secret(self.my_secret),
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
            secret=self.my_secret,
            target=instance1,  # a Connectable
            vpc=target_vpc,  # The VPC for secret rotation
            exclude_characters=" %+:;\{\}'\"\,@\\",
        )
