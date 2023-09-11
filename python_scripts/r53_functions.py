# https_setup.py


import boto3
import botocore
import logging


def modify_hosted_zone_alias(
    domain,
    action,
    subdomain,
    target_hosted_zone_id,
    target_dns_name,
):
    logging.info("Modify Hosted Zone alias record")

    r53_client = boto3.client("route53")

    response = get_hosted_zone(r53_client, domain)
    hosted_zone_id = response["HostedZones"][0]["Id"]

    logging.info("creating route53 alias record for load balancer")
    modify_alias(
        r53_client,
        hosted_zone_id,
        action,
        subdomain,
        target_hosted_zone_id,
        target_dns_name,
    )


def modify_alias(
    r53_client,
    hosted_zone_id,
    action,
    sub_domain,
    target_hosted_zone_id,
    target_dns_name,
):
    kwargs = {
        "HostedZoneId": hosted_zone_id,
        "ChangeBatch": {
            "Comment": "Modifying alias record for tplot app",
            "Changes": [
                {
                    "Action": action,
                    "ResourceRecordSet": {
                        "Name": sub_domain,
                        "Type": "A",
                        "AliasTarget": {
                            "HostedZoneId": target_hosted_zone_id,
                            "DNSName": target_dns_name,
                            "EvaluateTargetHealth": True,
                        },
                    },
                }
            ],
        },
    }
    try:
        response = r53_client.change_resource_record_sets(**kwargs)
        logging.info(
            f"Requested modify load balancer alias record {kwargs}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested modify load balancer alias record failed"
        )
        raise
    else:
        return response


def get_hosted_zone(r53_client, dns_name):
    try:
        response = r53_client.list_hosted_zones_by_name(DNSName=dns_name)
        logging.info(f"Requested list hosted zones by name for {dns_name}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested list hosted zones by name  failed")
        raise
    else:
        return response
