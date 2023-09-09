#!/usr/bin/env python3
# https_terminate.py


import boto3
import botocore
import logging


def request_certificate_for_domain(acm_client, domain_name, tags):
    kwargs = {
        "DomainName": domain_name,
        "ValidationMethod": "DNS",
        "Tags": tags,
    }
    try:
        response = acm_client.request_certificate(**kwargs)
        logging.info(f"Requested certificate for domain {domain_name}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested certificate for domain failed")
        raise
    else:
        return response


def get_lbs(lb_client, kwargs):
    try:
        response = lb_client.describe_load_balancers(**kwargs)
        logging.info(f"Requested describe load balancers with kwargs {kwargs}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested describe load balancers failed")
        raise
    else:
        return response


def get_lb_tags(lb_client, lb_arns):
    try:
        response = lb_client.describe_tags(ResourceArns=lb_arns)
        logging.info(f"Requested describe tags with {lb_arns}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested describe tag failed")
        raise
    else:
        return response


def get_lb(lb_client, env_name):
    lb_response = get_lbs(lb_client, {})
    for lb in lb_response["LoadBalancers"]:
        lb_arn = lb["LoadBalancerArn"]
        tag_response = get_lb_tags(lb_client, [lb_arn])
        for tag in tag_response["TagDescriptions"][0]["Tags"]:
            if tag["Key"] == "elasticbeanstalk:environment-name":
                if tag["Value"] == env_name:
                    return lb

    return None


def delete_alias_record_for_load_balancer(
    r53_client,
    hosted_zone_id,
    subdomain,
    lb_hosted_zone_id,
    lb_dns_name,
):
    kwargs = {
        "HostedZoneId": hosted_zone_id,
        "ChangeBatch": {
            "Comment": "Delete alias record to load balancer for tplot app",
            "Changes": [
                {
                    "Action": "DELETE",
                    "ResourceRecordSet": {
                        "Name": subdomain,
                        "Type": "A",
                        "AliasTarget": {
                            "HostedZoneId": lb_hosted_zone_id,
                            "DNSName": lb_dns_name,
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
            f"Requested delete of alias record for load balancer {kwargs}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested delete of alias record for load balancer failed"
        )
        raise
    else:
        return response


def list_certificates(acm_client):
    try:
        response = acm_client.list_certificates()
        logging.info("Requested list certificates")
    except botocore.exceptions.ClientError:
        logging.exception("Requested list certificates failed")
        raise
    else:
        return response


def get_certificate_arn(certificates, domain_name):
    for certificate in certificates:
        if certificate['DomainName'] == domain_name:
            return certificate['CertificateArn']
    return None


def delete_certificate(acm_client, certificate_arn):
    try:
        response = acm_client.delete_certificate(
            CertificateArn=certificate_arn
        )
        logging.info(
            f"Requested delete of certificate {certificate_arn}"
        )
    except botocore.exceptions.ClientError:
        logging.exception(
            "Requested delete of certificate failed"
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


def http_terminate(environment_name, domain, subdomain):

    logging.basicConfig(level=logging.INFO)

    lb_client = boto3.client("elbv2")

    logging.info("Getting load balancer")
    response = get_lb(lb_client, environment_name)
    lb_hosted_zone_id = response["CanonicalHostedZoneId"]
    lb_dns_name = response["DNSName"]

    r53_client = boto3.client("route53")

    logging.info("Getting route53 hosted zone")
    response = get_hosted_zone(r53_client, domain)
    hosted_zone_id = response["HostedZones"][0]["Id"]

    delete_alias_record_for_load_balancer(
        r53_client,
        hosted_zone_id,
        subdomain,
        lb_hosted_zone_id,
        lb_dns_name
    )

    acm_client = boto3.client('acm')

    logging.info("Getting certificates")
    response = list_certificates(acm_client)

    logging.info("Getting certificate arn")
    certificate_arn = get_certificate_arn(
        response['CertificateSummaryList'],
        f"*.{domain}"
    )

    if certificate_arn is not None:
        logging.info("Getting certificates arn")
        delete_certificate(acm_client, certificate_arn)
