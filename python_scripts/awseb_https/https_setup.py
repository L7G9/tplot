#!/usr/bin/env python3
# https_setup.py


import logging

from acm_functions import get_acm_certificate
from ec2_functions import add_https_ingress_to_security_group
from elb_functions import configure_load_balancer
from r53_functions import modify_hosted_zone_alias


def http_setup(environment_name, domain, subdomain):
    TAG_KEY = "aws_ebs_environment"
    TAGS = [
        {"Key": TAG_KEY, "Value": environment_name},
    ]

    logging.basicConfig(level=logging.INFO)

    print(f"Setting up HTTPS access for EBS environment {environment_name}")

    cert_arn = get_acm_certificate(domain, TAGS)

    add_https_ingress_to_security_group(environment_name)

    response = configure_load_balancer(environment_name, cert_arn, TAGS)
    lb_hosted_zone_id = response["CanonicalHostedZoneId"]
    lb_dns_name = response["DNSName"]

    modify_hosted_zone_alias(
        domain,
        'CREATE',
        subdomain,
        lb_hosted_zone_id,
        lb_dns_name
    )

    print(f"Success site is now available at https://{subdomain}")
