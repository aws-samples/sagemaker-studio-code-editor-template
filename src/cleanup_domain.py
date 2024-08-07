import boto3
import json
import logging
import time
import cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)
sagemaker = boto3.client("sagemaker")


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    domain_id = event["ResourceProperties"]["DomainId"]
    physical_resource_id = f"{domain_id}-cleanup"
    request_type = event["RequestType"]

    try:
        # create / update
        if request_type in ["Create", "Update"]:
            send_success(event, context, {}, physical_resource_id)

        # delete
        elif request_type == "Delete":
            delete_domain(domain_id)
            logger.info(f"Domain '{domain_id}' has been deleted.")
            time.sleep(10)  # wait for eni to be deleted
            send_success(event, context, {}, physical_resource_id)

    except Exception as e:
        send_failure(event, context, e)


def send_failure(event, context, e):
    logger.error(e)
    cfnresponse.send(event, context, cfnresponse.FAILED, {"Error": str(e)}, event.get("PhysicalResourceId"), reason=str(e))


def send_success(event, context, data, physical_resource_id):
    cfnresponse.send(event, context, cfnresponse.SUCCESS, data, physical_resource_id)


def wait_for_domain_stability(domain_id, desired_status=None):
    while True:
        res = sagemaker.describe_domain(DomainId=domain_id)
        status = res["Status"]  # 'Deleting'|'Failed'|'InService'|'Pending'|'Updating'|'Update_Failed'|'Delete_Failed'
        if desired_status and status == desired_status:
            break
        if status in ["Failed", "Update_Failed", "Delete_Failed"]:
            raise RuntimeError(f"Space is in '{status}' state.")
        else:
            time.sleep(10)
    return res


def delete_domain(domain_id):
    try:
        sagemaker.delete_domain(DomainId=domain_id, RetentionPolicy={"HomeEfsFileSystem": "Delete"})
        wait_for_domain_stability(domain_id, "Deleted")
    except sagemaker.exceptions.ResourceNotFound as e:
        logger.info(f"Domain '{domain_id}' has been deleted. Recovering from exception: {str(e)}")
    except Exception as e:
        raise e
