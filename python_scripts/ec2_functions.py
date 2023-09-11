# ec2_functions.py


import boto3
import botocore
import logging


def get_security_group(ec2_client, kwargs):
    try:
        response = ec2_client.describe_security_groups(**kwargs)
        logging.info(f"Requested describe security group with kwargs {kwargs}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested describe security group failed")
        raise
    else:
        return response


def add_ingress_permissions(ec2_client, security_group_id, ip_permissions):
    try:
        response = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id, IpPermissions=ip_permissions
        )
        success = response["Return"]
        logging.info(
            f"Requested authorize ingress rule for {security_group_id}"
        )
    except botocore.exceptions.ClientError:
        logging.exception("Requested authorize ingress rule failed")
        raise
    else:
        return success


def add_https_ingress_to_security_group(environment_name):
    logging.info(f"Adding HTTPS ingress rule to load balancer Security Group\
                  in {environment_name}")

    ec2_client = boto3.client("ec2")

    kwargs = {
        "Filters": [
            {
                "Name": "tag:elasticbeanstalk:environment-name",
                "Values": [environment_name],
            },
            {
                "Name": "tag:aws:cloudformation:logical-id",
                "Values": ["AWSEBLoadBalancerSecurityGroup"],
            },
        ]
    }
    response = get_security_group(ec2_client, kwargs)
    security_group_id = response["SecurityGroups"][0]["GroupId"]

    ip_permissions = [
        {
            "FromPort": 443,
            "ToPort": 443,
            "IpProtocol": "tcp",
            "IpRanges": [
                {"CidrIp": "0.0.0.0/0", "Description": "Allow HTTPS inbound"}
            ],
        }
    ]
    return add_ingress_permissions(
        ec2_client, security_group_id, ip_permissions
    )
