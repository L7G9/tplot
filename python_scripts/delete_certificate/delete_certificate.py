#!/usr/bin/env python3
# delete_certificate.py


import logging


from acm_functions import delete_acm_certificate


def delete_domain_certificate(domain):

    logging.basicConfig(level=logging.INFO)

    print(f"Deleting ACM Certificate for {domain}")

    delete_acm_certificate(domain)
