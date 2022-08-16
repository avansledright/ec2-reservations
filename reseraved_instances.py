import boto3
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError
import os
import json
ec2_client = boto3.client("ec2", region_name="us-west-2")

def get_reserved_instances():
    response = ec2_client.describe_reserved_instances()
    reserved_instances = {}
    for reservedInstances in response['ReservedInstances']:
        reserved_instances.update({
            reservedInstances['ReservedInstancesId']: {
                "ExpireDate": reservedInstances['End'],
                "Type": reservedInstances['InstanceType']
            }
        })
    return reserved_instances
def determine_expirery(expirery_date):
    now = datetime.now(timezone.utc)
    delta_min = timedelta(days=21)
    delta_max = timedelta(days=22)
    if expirery_date - now >= delta_min and expirery_date - now < delta_max:
        return True
    else:
        return False
#Send Result to SNS
def sendToSNS(messages):
    sns = boto3.client('sns')
    try:
        send_message = sns.publish(
            TargetArn=os.environ['SNS_TOPIC'],
            Subject='EC2-Reservation',
            Message=messages,
            )
        return send_message
    except ClientError as e:
        print("Failed to send message to SNS")
        print(e)


if __name__ == "__main__":

    for reservation, res_details in get_reserved_instances().items():
        if determine_expirery(res_details['ExpireDate']) == True:
            sns_message = {"reservation": reservation, "expires": res_details['ExpireDate'].strftime("%m/%d/%Y, %H:%M:%S")}
            sendToSNS(json.dumps(sns_message))
#  