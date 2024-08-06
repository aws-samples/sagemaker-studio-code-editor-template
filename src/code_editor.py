import boto3
import json
import logging
import time
import cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)
sagemaker = boto3.client("sagemaker")

SPACE_NAME = "default"
APP_NAME = "default"


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    domain_id = event["ResourceProperties"]["DomainId"]
    user_profile_name = event["ResourceProperties"]["UserProfileName"]
    instance_type = event["ResourceProperties"]["InstanceType"]
    sagemaker_image_arn = event["ResourceProperties"]["SageMakerImageArn"]
    lifecycle_config_arn = event["ResourceProperties"]["LifecycleConfigArn"]
    ebs_size = int(event["ResourceProperties"]["EbsSizeInGb"])
    request_type = event["RequestType"]
    physical_resource_id = f"{domain_id}-codeeditor"

    try:
        # create
        if request_type == "Create":
            # create space
            create_space(
                domain_id,
                SPACE_NAME,
                user_profile_name,
                ebs_size,
                instance_type,
                sagemaker_image_arn,
                lifecycle_config_arn,
            )
            logger.info(f"Space '{SPACE_NAME}' has been created: 'EbsSizeInGb={ebs_size},InstanceType={instance_type}'")
            # create app
            create_app(domain_id, SPACE_NAME, APP_NAME, instance_type, sagemaker_image_arn, lifecycle_config_arn)
            logger.info(f"App '{APP_NAME}' has been created: 'InstanceType={instance_type}'")
            send_success(event, context, {}, physical_resource_id)

        # update
        elif request_type == "Update":
            # see if space should be updated
            space_instance_type_updated = False
            space_ebs_size_updated = False

            # see if ebs size has been updated
            res = sagemaker.describe_space(DomainId=domain_id, SpaceName=SPACE_NAME)
            current_ebs_size = int(res["SpaceSettings"]["SpaceStorageSettings"]["EbsStorageSettings"]["EbsVolumeSizeInGb"])
            # fail if ebs size has been descreased
            if ebs_size < current_ebs_size:
                e = ValueError("The decrease of 'EbsVolumeSizeInGb' is not supported.")
                raise e
            elif ebs_size > current_ebs_size:
                space_ebs_size_updated = True

            # see if instance type has been updated
            current_instance_type = res["SpaceSettings"]["CodeEditorAppSettings"]["DefaultResourceSpec"]["InstanceType"]
            if current_instance_type != instance_type:
                space_instance_type_updated = True

            # see if app should be updated
            app_updated = False
            res = describe_app(domain_id=domain_id, space_name=SPACE_NAME, app_name=APP_NAME)
            if not res or res["Status"] in ["Deleted", "Deleting"] or res["ResourceSpec"]["InstanceType"] != instance_type:
                app_updated = True

            # delete existing app (we cannot update EBS storage while app is in service)
            if space_ebs_size_updated or app_updated:
                delete_app(domain_id, SPACE_NAME, APP_NAME)
                logger.info(f"App '{APP_NAME}' has been deleted.")
                time.sleep(10)  # wait for app to be ready

            # update space
            if space_ebs_size_updated or space_instance_type_updated:
                update_space(domain_id, SPACE_NAME, ebs_size, instance_type)
                logger.info(f"Space '{SPACE_NAME}' has been updated: 'EbsSizeInGb={ebs_size},InstanceType={instance_type}'")
                time.sleep(10)  # wait for space to be ready

            # recreate app
            if space_ebs_size_updated or app_updated:
                create_app(domain_id, SPACE_NAME, APP_NAME, instance_type, sagemaker_image_arn, lifecycle_config_arn)
                logger.info(f"App '{APP_NAME}' has been created again: 'InstanceType={instance_type}'")

            send_success(event, context, {}, physical_resource_id)

        # delete
        elif request_type == "Delete":
            # delete app
            delete_app(domain_id, SPACE_NAME, APP_NAME)
            logger.info(f"App '{APP_NAME}' has been deleted.")
            # delete space
            delete_space(domain_id, SPACE_NAME)
            logger.info(f"Space '{SPACE_NAME}' has been deleted.")
            send_success(event, context, {}, physical_resource_id)

    except Exception as e:
        send_failure(event, context, e)


def send_failure(event, context, e):
    logger.error(e)
    cfnresponse.send(event, context, cfnresponse.FAILED, {"Error": str(e)}, event.get("PhysicalResourceId"), reason=str(e))


def send_success(event, context, data, physical_resource_id):
    cfnresponse.send(event, context, cfnresponse.SUCCESS, data, physical_resource_id)


def wait_for_space_stability(domain_id, space_name, desired_status=None):
    while True:
        res = sagemaker.describe_space(DomainId=domain_id, SpaceName=space_name)
        status = res["Status"]  # 'Deleting'|'Failed'|'InService'|'Pending'|'Updating'|'Update_Failed'|'Delete_Failed'
        if desired_status and status == desired_status:
            break
        if status in ["Failed", "Update_Failed", "Delete_Failed"]:
            raise RuntimeError(f"Space is in '{status}' state.")
        else:
            time.sleep(10)
    return res


def create_space(
    domain_id,
    space_name,
    user_profile_name,
    ebs_size,
    instance_type,
    sagemaker_image_arn,
    lifecycle_config_arn,
):
    sagemaker.create_space(
        DomainId=domain_id,
        SpaceName=space_name,
        SpaceSettings={
            "AppType": "CodeEditor",
            "SpaceStorageSettings": {"EbsStorageSettings": {"EbsVolumeSizeInGb": ebs_size}},
            "CodeEditorAppSettings": {
                "DefaultResourceSpec": {
                    "SageMakerImageArn": sagemaker_image_arn,
                    "InstanceType": instance_type,
                    "LifecycleConfigArn": lifecycle_config_arn,
                }
            },
        },
        OwnershipSettings={"OwnerUserProfileName": user_profile_name},
        SpaceSharingSettings={"SharingType": "Private"},
        SpaceDisplayName=space_name,
    )
    return wait_for_space_stability(domain_id, space_name, "InService")


def update_space(domain_id, space_name, ebs_size, instance_type):
    sagemaker.update_space(
        DomainId=domain_id,
        SpaceName=space_name,
        SpaceSettings={
            "SpaceStorageSettings": {"EbsStorageSettings": {"EbsVolumeSizeInGb": ebs_size}},
            "CodeEditorAppSettings": {"DefaultResourceSpec": {"InstanceType": instance_type}},
        },
    )
    return wait_for_space_stability(domain_id, space_name, "InService")


def delete_space(domain_id, space_name):
    try:
        spaces = sagemaker.list_spaces(DomainIdEquals=domain_id)["Spaces"]
        spaces = [space for space in spaces if space["SpaceName"] == space_name]
        for space in spaces:
            if space["Status"] != "Deleting":
                sagemaker.delete_space(
                    DomainId=domain_id,
                    SpaceName=space_name,
                )
            wait_for_space_stability(domain_id, space_name)
    except sagemaker.exceptions.ResourceNotFound as e:
        logger.info(f"Space '{space_name}' has beed deleted. Recovering from exception: {str(e)}")
    except Exception as e:
        raise e


def wait_for_app_stability(domain_id, space_name, app_name, desired_status=None):
    while True:
        res = sagemaker.describe_app(DomainId=domain_id, AppType="CodeEditor", AppName=app_name, SpaceName=space_name)
        status = res["Status"]  # 'Deleted'|'Deleting'|'Failed'|'InService'|'Pending'
        if desired_status and status == desired_status:
            break
        if status in ["Failed"]:
            raise RuntimeError(f"Space is in '{status}' state.")
        else:
            time.sleep(10)
    return res


def create_app(domain_id, space_name, app_name, instance_type, sagemaker_image_arn, lifecycle_config_arn):
    sagemaker.create_app(
        DomainId=domain_id,
        SpaceName=space_name,
        AppType="CodeEditor",
        AppName=app_name,
        ResourceSpec={
            "InstanceType": instance_type,
            "SageMakerImageArn": sagemaker_image_arn,
            "LifecycleConfigArn": lifecycle_config_arn,
        },
    )
    return wait_for_app_stability(domain_id, space_name, app_name, "InService")


def describe_app(domain_id, space_name, app_name):
    try:
        return sagemaker.describe_app(
            DomainId=domain_id,
            AppType="CodeEditor",
            AppName=app_name,
            SpaceName=space_name,
        )
    except sagemaker.exceptions.ResourceNotFound as e:
        # allow manual deletion of code editor app as it is considered short-lived
        logger.info(f"App '{APP_NAME}' has been deleted. Recovering from exception: {str(e)}")
        return None
    except Exception as e:
        raise e


def delete_app(domain_id, space_name, app_name):
    try:
        apps = sagemaker.list_apps(DomainIdEquals=domain_id, SpaceNameEquals=space_name)["Apps"]
        apps = [app for app in apps if app["AppName"] == app_name]
        for app in apps:
            if app["Status"] not in ["Deleted", "Deleting"]:
                sagemaker.delete_app(
                    DomainId=domain_id,
                    SpaceName=space_name,
                    AppType="CodeEditor",
                    AppName=app_name,
                )
            wait_for_app_stability(domain_id, space_name, app_name, "Deleted")
    except sagemaker.exceptions.ResourceNotFound as e:
        logger.info(f"App '{app_name}' has been deleted. Recovering from exception: {str(e)}")
    except Exception as e:
        raise e
