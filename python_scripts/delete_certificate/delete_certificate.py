#!/usr/bin/env python3
# delete_certificate.py


import boto3
import botocore
import logging


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


def delete_acm_certificate(acm_client, certificate_arn):
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


def delete_certificate(domain):

    logging.basicConfig(level=logging.INFO)

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
        delete_acm_certificate(acm_client, certificate_arn)
