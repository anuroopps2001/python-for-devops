import boto3
import json

# get ec2 details in specific region
ec2 = boto3.client('ec2', region_name='us-east-1')

response = ec2.describe_instances()
print(json.dumps(response, indent=4, default=str, skipkeys=True))

print("=============")

for reservation in response['Reservations']:
     for instance in reservation['Instances']:
         print(
# When you put an f before the opening quote, it tells Python: "Look inside this string for curly braces {}. 
# If you find them, evaluate the code inside and stick the result right there."
    f"Instance ID: {instance['InstanceId']} is {instance['State']['Name']} in VPC: {instance['VpcId']}\n"
    f"and subnet: {instance['SubnetId']} having blockMapping device of "
    f"{instance['BlockDeviceMappings'][0]['DeviceName']}"
)