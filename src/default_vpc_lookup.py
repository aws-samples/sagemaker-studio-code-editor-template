import boto3
import json
import logging
import cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ec2 = boto3.client("ec2")


def lambda_handler(event, context):
    physical_resource_id = "default-vpc-lookup"
    logger.info(f"Received event: {json.dumps(event)}")
    try:
        if event["RequestType"] in ["Create", "Update"]:
            # get default vpc id
            res = ec2.describe_vpcs(Filters=[{"Name": "isDefault", "Values": ["true"]}])
            vpc_id = res["Vpcs"][0]["VpcId"]
            # get subnet ids
            res = ec2.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])
            subnet_ids = ",".join([subnet["SubnetId"] for subnet in res["Subnets"]])
            data = {"VpcId": vpc_id, "SubnetIds": subnet_ids}
            send_success(event, context, data, physical_resource_id)
        elif event["RequestType"] == "Delete":
            send_success(event, context, {}, physical_resource_id)

    except Exception as e:
        send_failure(event, context, e)


def send_failure(event, context, e):
    logger.error(e)
    cfnresponse.send(event, context, cfnresponse.FAILED, {"Error": str(e)}, event.get("PhysicalResourceId"), reason=str(e))


def send_success(event, context, data, physical_resource_id):
    cfnresponse.send(event, context, cfnresponse.SUCCESS, data, physical_resource_id)
