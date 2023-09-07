#!/usr/bin/env python3
# https_setup.py


import boto3
import botocore
import logging


def get_security_group(ec2_client, kwargs):
    try:
        response = ec2_client.describe_security_groups(**kwargs)
        logging.info(
            f"Requested describe security group with kwargs {kwargs}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested describe security group failed"
        )
        raise
    else:
        return response


def add_ingress_permissions(ec2_client, security_group_id, ip_permissions):
    try:
        response = ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=ip_permissions
        )
        success = response['Return']
        logging.info(
            f"Requested authorize security group ingress for {security_group_id}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested authorize security group ingress failed"
        )
        raise
    else:
        return success


def add_https_ingress_to_security_group(ec2_client, env_name):
    kwargs = {
        "Filters": [
            {
                "Name": "tag:elasticbeanstalk:environment-name",
                "Values": [env_name]
            },
            {
                "Name": "tag:aws:cloudformation:logical-id",
                "Values": ["AWSEBLoadBalancerSecurityGroup"]
            },
        ]
    }
    response = get_security_group(ec2_client, kwargs)
    security_group_id = response['SecurityGroups'][0]['GroupId']

    ip_permissions = [
        {
            'FromPort': 443,
            'ToPort': 443,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': '0.0.0.0/0',
                    'Description': 'Allow HTTPS inbound'
                }
            ]
        }
    ]
    return add_ingress_permissions(
        ec2_client,
        security_group_id,
        ip_permissions
    )


def get_lbs(lb_client, kwargs):
    try:
        response = lb_client.describe_load_balancers(**kwargs)
        logging.info(
            f"Requested describe load balancers with kwargs {kwargs}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested describe load balancers failed"
        )
        raise
    else:
        return response


def get_lb_tags(lb_client, lb_arns):
    try:
        response = lb_client.describe_tags(ResourceArns=lb_arns)
        logging.info(
            f"Requested describe tags with {lb_arns}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested describe tag failed"
        )
        raise
    else:
        return response


def get_lb(lb_client, env_name):
    lb_response = get_lbs(lb_client, {})
    for lb in lb_response['LoadBalancers']:
        lb_arn = lb['LoadBalancerArn']
        tag_response = get_lb_tags(lb_client, [lb_arn])
        for tag in tag_response['TagDescriptions'][0]['Tags']:
            if tag['Key'] == 'elasticbeanstalk:environment-name':
                if tag['Value'] == env_name:
                    return lb

    return None


def get_lb_listeners(lb_client, lb_arn):
    try:
        response = lb_client.describe_listeners(LoadBalancerArn=lb_arn)
        logging.info(
            f"Requested describe listeners with {lb_arn}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested describe listeners failed"
        )
        raise
    else:
        return response


def modify_listener_redirect_http_to_https(lb_client, lb_arn):
    listeners_response = get_lb_listeners(lb_client, lb_arn)
    http_listener_arn = listeners_response['Listeners'][0]['ListenerArn']

    default_actions = [
        {
            'Type': 'redirect',
            'RedirectConfig': {
                'Protocol': 'HTTPS',
                'Port': '443',
                'StatusCode': 'HTTP_301'
            },
        }
    ]

    kwargs = {
        'ListenerArn': http_listener_arn,
        'DefaultActions': default_actions,
    }

    try:
        response = lb_client.modify_listener(**kwargs)
        logging.info(
            f"Requested modify listener with {kwargs}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested modify listener failed"
        )
        raise
    else:
        return response


def create_listener_forward_https_to_target_group(
    lb_client,
    lb_arn,
    tg_arn,
    certificate_arn,
    tags
):
    default_actions = [
        {
            'Type': 'forward',
            'TargetGroupArn': tg_arn,
        }
    ]

    kwargs = {
        'LoadBalancerArn': lb_arn,
        'Protocol': 'HTTPS',
        'Port': 443,
        'Certificates': [{'CertificateArn': certificate_arn}],
        'DefaultActions': default_actions,
        'Tags': tags
    }

    try:
        response = lb_client.create_listener(**kwargs)
        logging.info(
            f"Requested create listener with {kwargs}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested create listener failed"
        )
        raise
    else:
        return response


def get_load_balancer_target_groups(lb_client, lb_arn):
    kwargs = {
        'LoadBalancerArn': lb_arn
    }
    try:
        response = lb_client.describe_target_groups(**kwargs)
        logging.info(
            f"Requested describe target groups with {kwargs}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested describe target groups failed"
        )
        raise
    else:
        return response


def request_certificate_for_domain(acm_client, domain_name, tags):
    kwargs = {
        'DomainName': domain_name,
        'ValidationMethod': 'DNS',
        'Tags': tags
    }
    try:
        response = acm_client.request_certificate(**kwargs)
        logging.info(
            f"Requested certificate for domain {domain_name}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested certificate for domain failed"
        )
        raise
    else:
        return response


def create_alias_record_for_load_balancer(
    r53_client,
    hosted_zone_id,
    sub_domain,
    lb_hosted_zone_id,
    lb_dns_name,
):
    kwargs = {
        'HostedZoneId': hosted_zone_id,
        'ChangeBatch': {
            'Comment': 'Adding alias record to load balancer for tplot app',
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': sub_domain,
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': lb_hosted_zone_id,
                            'DNSName': lb_dns_name,
                            'EvaluateTargetHealth': True
                        },
                    }
                }
            ],
        }
    }
    try:
        response = r53_client.change_resource_record_sets(**kwargs)
        logging.info(
            f"Requested create of alias record for load balancer {kwargs}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested create of alias record for load balancer failed"
        )
        raise
    else:
        return response


def get_hosted_zone(r53_client, dns_name):
    try:
        response = r53_client.list_hosted_zones_by_name(DNSName=dns_name)
        logging.info(
            f"Requested list hosted zones by name for {dns_name}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested list hosted zones by name  failed"
        )
        raise
    else:
        return response


def main():
    ENVIRONMENT_NAME = 'tplot-prod'
    DOMAIN = 'lukegregorydev.co.uk'
    SUBDOMAIN = 'tplot.lukegregorydev.co.uk'
    TAG_KEY = 'aws_ebs_environment'
    TAGS = [
        {
            'Key': TAG_KEY,
            'Value': ENVIRONMENT_NAME
        },
    ]

    logging.basicConfig(level=logging.INFO)

    print(f"Setting up HTTPS access for EBS environment {ENVIRONMENT_NAME}")

    acm_client = boto3.client("acm")

    logging.info(f"Requesting certificate for domain *.{DOMAIN}")
    response = request_certificate_for_domain(
        acm_client,
        f"*.{DOMAIN}",
        TAGS
    )
    cert_arn = response['CertificateArn']

    logging.info("Waiting for certificate to be validated...")
    waiter = acm_client.get_waiter('certificate_validated')
    waiter.wait(CertificateArn=cert_arn)
    logging.info("Certificate to be validated")

    ec2_client = boto3.client("ec2")

    logging.info("Updating security groups")
    add_https_ingress_to_security_group(ec2_client, ENVIRONMENT_NAME)

    lb_client = boto3.client('elbv2')

    logging.info("Getting load balancer")
    response = get_lb(lb_client, ENVIRONMENT_NAME)
    lb_arn = response['LoadBalancerArn']
    lb_hosted_zone_id = response['CanonicalHostedZoneId']
    lb_dns_name = response['DNSName']

    logging.info("Getting load balancer target groups")
    response = get_load_balancer_target_groups(lb_client, lb_arn)
    target_group_arn = response['TargetGroups'][0]['TargetGroupArn']

    logging.info("Updating load balancer http listener")
    modify_listener_redirect_http_to_https(lb_client, lb_arn)

    logging.info("Creating load balancer https listener")
    create_listener_forward_https_to_target_group(
        lb_client,
        lb_arn,
        target_group_arn,
        cert_arn,
        TAGS
    )

    logging.info("Getting route53 hosted zone")
    r53_client = boto3.client('route53')
    response = get_hosted_zone(r53_client, DOMAIN)
    hosted_zone_id = response['HostedZones'][0]['Id']

    logging.info("creating route53 alias record for load balancer")
    create_alias_record_for_load_balancer(
        r53_client,
        hosted_zone_id,
        SUBDOMAIN,
        lb_hosted_zone_id,
        lb_dns_name
    )

    print(f"Success site is now available at https://{SUBDOMAIN}")


if __name__ == "__main__":
    main()
