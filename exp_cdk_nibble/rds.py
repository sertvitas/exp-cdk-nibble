from aws_cdk import Stack, aws_secretsmanager as sm, aws_rds as rds, aws_ec2 as ec2
from constructs import Construct


class RdsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        my_secret = sm.Secret(self, "Secret"
                              )
        my_vpc = ec2.Vpc.from_lookup(
            self, "cts_vpc", vpc_name="TheVPC"
        )
        instance1 = rds.DatabaseInstance(self, "PostgresInstance1",
                                         engine=rds.DatabaseInstanceEngine.POSTGRES,
                                         credentials=rds.Credentials.from_secret(my_secret),
                                         vpc=my_vpc
                                         )
        sm.SecretRotation(self, "SecretRotation",
                          application=sm.SecretRotationApplication.POSTGRES_ROTATION_SINGLE_USER,
                          # Postgres single user scheme
                          secret=my_secret,
                          target=instance1,  # a Connectable
                          vpc=my_vpc,  # The VPC where the secret rotation application will be deployed
                          exclude_characters=" %+:;{}"
                          )
