import boto3
from TaggedInstancePool import TaggedInstancePool


def lambda_handler(event, context):
    iscore = TaggedInstancePool("isCore")
    ec2 = boto3.client('ec2')

    startInstances = ec2.start_instances(
        InstanceIds=iscore.haves,
        DryRun=False
    )

    response = {
        "StartInstances": iscore.haves
    }

    return response
