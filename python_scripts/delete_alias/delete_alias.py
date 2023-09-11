#!/usr/bin/env python3
# delete_alias.py

import boto3
import logging

from elb_functions import get_load_balancer
from r53_functions import modify_hosted_zone_alias


def delete_load_balancer_alias_record(environment_name, domain, subdomain):

    logging.basicConfig(level=logging.INFO)

    print(f"Deleting Load Balancer alias record in {environment_name}")

    lb_client = boto3.client("elbv2")

    response = get_load_balancer(lb_client, environment_name)
    lb_hosted_zone_id = response["CanonicalHostedZoneId"]
    lb_dns_name = response["DNSName"]

    modify_hosted_zone_alias(
        domain,
        "DELETE",
        subdomain,
        lb_hosted_zone_id,
        lb_dns_name
    )
