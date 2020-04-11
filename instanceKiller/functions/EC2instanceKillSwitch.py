import boto3
from TaggedInstancePool import TaggedInstancePool


def lambda_handler(event, context):
    isdontstop = TaggedInstancePool("isDontStop")
    ec2 = boto3.client('ec2')

    stopInstances = ec2.stop_instances(
        InstanceIds=isdontstop.havenots,
        DryRun=False
    )

    response = {
        "StopInstances": isdontstop.havenots
    }
