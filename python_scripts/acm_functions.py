# acm functions.py


import boto3
import botocore
import logging


def get_acm_certificate(domain, tags):
    logging.info(f"Get ACM certificate for domain {domain}")

    acm_client = boto3.client("acm")

    response = request_certificate_for_domain(
        acm_client, f"*.{domain}",
        tags
    )
    certificate_arn = response["CertificateArn"]

    wait_for_certificate_validation(acm_client, certificate_arn)

    return certificate_arn


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


def wait_for_certificate_validation(acm_client, certificate_arn):
    logging.info("Waiting for certificate to be validated...")
    waiter = acm_client.get_waiter("certificate_validated")
    waiter.wait(CertificateArn=certificate_arn)
    logging.info("Certificate to be validated")


def delete_acm_certificate(domain):
    logging.info(f"Delete ACM certificate for domain {domain}")

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
