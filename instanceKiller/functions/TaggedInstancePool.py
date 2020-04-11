import boto3


class TaggedInstancePool:

    def __init__(self, tag):
        # ec2 = boto3.client('ec2')
        session = boto3.Session(profile_name='ctcs')
        ec2 = session.client('ec2')

        all_instances = ec2.describe_instances()
        all_instances_set = set(ec2['InstanceId'] for resId in all_instances['Reservations']
                                for ec2 in resId['Instances'])

        with_tag = ec2.describe_instances(
            Filters=[{'Name': 'tag:' + tag, 'Values': ['True']}]
        )
        with_tag_set = set(ec2['InstanceId'] for resId in with_tag['Reservations']
                           for ec2 in resId['Instances'])

        without_tag_set = all_instances_set - with_tag_set

        self.havenots = list(without_tag_set)
        self.haves = list(with_tag_set)
        self.all = list(all_instances_set)


if __name__ == "__main__":
    instances = TaggedInstancePool("isCore")

    print("all:{} \n".format(instances.all))
    print("have:{} \n".format(instances.haves))
    print("havenots:{} \n".format(instances.havenots))
