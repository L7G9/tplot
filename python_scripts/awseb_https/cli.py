# cli.py
"""VPC Tree application's Command Line Interface."""

import argparse

from . import https_setup

from . import __version__


def main():
    """"""
    args = parse_cmd_line_arguments()

    if args.terminate:
        print(f"terminate {args.environment_name[0]} {args.domain[0]} {args.subdomain[0]}")
    else:
        print(f"setup {args.environment_name[0]} {args.domain[0]} {args.subdomain[0]}")
        #https_setup.http_setup(
        #    args.environment_name,
        #    args.domain,
        #    args.subdomain
        #)


def parse_cmd_line_arguments():
    """"""
    parser = argparse.ArgumentParser(
        prog="awseb_https",
        description="Setup HTTPS access for an AWS Elastic Beanstalk Application Load Balancer",
        epilog="Thanks for using Setup HTTPS.",
    )
    parser.version = f"VPC Tree V{__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "-t",
        "--terminate",
        required=False,
        action="store_true",
        help="Remove AWS resources created ",
    )

    parser.add_argument(
        "-e",
        "--environment_name",
        required=True,
        nargs=1,
        help="Name of Elastic Beanstalk environment",
    )

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        nargs=1,
        help="Name of the Route53 domain",
    )

    parser.add_argument(
        "-s",
        "--subdomain",
        required=True,
        nargs=1,
        help="Name of the subdomain to create in Route53 domain",
    )

    return parser.parse_args()
