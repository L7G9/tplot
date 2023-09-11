# cli.py
"""Delete Certficate Script's Command Line Interface."""

import argparse

from . import delete_certificate
from . import __version__


def main():
    """"""
    args = parse_cmd_line_arguments()

    delete_certificate.delete_domain_certificate(args.domain[0])


def parse_cmd_line_arguments():
    """"""
    parser = argparse.ArgumentParser(
        prog="awseb_https",
        description="Delete ACM certificate created by https_setup.py",
        epilog="Thanks for using Delete Certificate.",
    )
    parser.version = f"VPC Tree V{__version__}"
    parser.add_argument("-v", "--version", action="version")

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        nargs=1,
        help="Name of the Route53 domain",
    )

    return parser.parse_args()
