# cli.py
"""Delete Alias Script's Command Line Interface."""

import argparse

from . import delete_alias
from . import __version__


def main():
    """"""
    args = parse_cmd_line_arguments()

    delete_alias.delete_alias_record(
        args.environment_name[0],
        args.domain[0],
        args.subdomain[0]
    )


def parse_cmd_line_arguments():
    """"""
    parser = argparse.ArgumentParser(
        prog="delete_alias",
        description="Delete Route53 alias record created by https_setup.py",
        epilog="Thanks for using Delete Alias.",
    )
    parser.version = f"VPC Tree V{__version__}"
    parser.add_argument("-v", "--version", action="version")

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
        help="Name of the subdomain in Route53 domain",
    )

    return parser.parse_args()
