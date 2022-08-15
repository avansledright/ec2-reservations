import boto3
from datetime import datetime, timezone, timedelta
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



if __name__ == "__main__":

    for reservation, res_details in get_reserved_instances().items():
        if determine_expirery(res_details['ExpireDate']) == True:
            print(reservation)
            print("I'm going to expire soon")
        else:
            print(reservation)
            print(res_details['ExpireDate'])