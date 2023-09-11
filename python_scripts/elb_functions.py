# elb_functions.py


import boto3
import botocore
import logging


def configure_load_balancer(environment_name, certificate_arn, tags):
    logging.info(f"Configure load balancer in {environment_name} to use HTTPS")

    lb_client = boto3.client("elbv2")

    logging.info("Getting load balancer")
    lb_response = get_load_balancer(lb_client, environment_name)
    lb_arn = lb_response["LoadBalancerArn"]

    logging.info("Getting load balancer target groups")
    response = get_load_balancer_target_groups(lb_client, lb_arn)
    target_group_arn = response["TargetGroups"][0]["TargetGroupArn"]

    logging.info("Updating load balancer http listener")
    modify_listener_redirect_http_to_https(lb_client, lb_arn)

    logging.info("Creating load balancer https listener")
    create_listener_forward_https_to_target_group(
        lb_client, lb_arn, target_group_arn, certificate_arn, tags
    )

    return lb_response


def get_load_balancers(lb_client, kwargs):
    try:
        response = lb_client.describe_load_balancers(**kwargs)
        logging.info(f"Requested describe load balancers with kwargs {kwargs}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested describe load balancers failed")
        raise
    else:
        return response


def get_load_balancer_tags(lb_client, lb_arns):
    try:
        response = lb_client.describe_tags(ResourceArns=lb_arns)
        logging.info(f"Requested describe tags with {lb_arns}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested describe tag failed")
        raise
    else:
        return response


def get_load_balancer(lb_client, env_name):
    lb_response = get_load_balancers(lb_client, {})
    for lb in lb_response["LoadBalancers"]:
        lb_arn = lb["LoadBalancerArn"]
        tag_response = get_load_balancer_tags(lb_client, [lb_arn])
        for tag in tag_response["TagDescriptions"][0]["Tags"]:
            if tag["Key"] == "elasticbeanstalk:environment-name":
                if tag["Value"] == env_name:
                    return lb

    return None


def get_load_balancer_listeners(lb_client, lb_arn):
    try:
        response = lb_client.describe_listeners(LoadBalancerArn=lb_arn)
        logging.info(f"Requested describe listeners with {lb_arn}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested describe listeners failed")
        raise
    else:
        return response


def modify_listener_redirect_http_to_https(lb_client, lb_arn):
    listeners_response = get_load_balancer_listeners(lb_client, lb_arn)
    http_listener_arn = listeners_response["Listeners"][0]["ListenerArn"]

    default_actions = [
        {
            "Type": "redirect",
            "RedirectConfig": {
                "Protocol": "HTTPS",
                "Port": "443",
                "StatusCode": "HTTP_301",
            },
        }
    ]

    kwargs = {
        "ListenerArn": http_listener_arn,
        "DefaultActions": default_actions,
    }

    try:
        response = lb_client.modify_listener(**kwargs)
        logging.info(f"Requested modify listener with {kwargs}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested modify listener failed")
        raise
    else:
        return response


def create_listener_forward_https_to_target_group(
    lb_client, lb_arn, tg_arn, certificate_arn, tags
):
    default_actions = [
        {
            "Type": "forward",
            "TargetGroupArn": tg_arn,
        }
    ]

    kwargs = {
        "LoadBalancerArn": lb_arn,
        "Protocol": "HTTPS",
        "Port": 443,
        "Certificates": [{"CertificateArn": certificate_arn}],
        "DefaultActions": default_actions,
        "Tags": tags,
    }

    try:
        response = lb_client.create_listener(**kwargs)
        logging.info(f"Requested create listener with {kwargs}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested create listener failed")
        raise
    else:
        return response


def get_load_balancer_target_groups(lb_client, lb_arn):
    kwargs = {"LoadBalancerArn": lb_arn}
    try:
        response = lb_client.describe_target_groups(**kwargs)
        logging.info(f"Requested describe target groups with {kwargs}")
    except botocore.exceptions.ClientError:
        logging.exception("Requested describe target groups failed")
        raise
    else:
        return response
