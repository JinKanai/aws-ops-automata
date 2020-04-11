import boto3
from TaggedInstancePool import TaggedInstancePool


class InstancePropertiesUtil:
    @classmethod
    def get_owner(cls, session, instance_id):
        return cls.get_tag_value(session, instance_id, "owner")

    @classmethod
    def get_launch_date(cls, session, instance_id):
        return session.Instance(instance_id).launch_time

    @classmethod
    def get_name(cls, session, instance_id):
        return cls.get_tag_value(session, instance_id, "name")

    @classmethod
    def get_tag_value(cls, session, instance_id, key):
        value = None
        instance_tags = session.Instance(instance_id).tags
        for tag in instance_tags:
            if tag["Key"].lower() == key:
                value = tag["Value"]
                break
        return value


if __name__ == '__main__':
    s = boto3.Session(profile_name="ctcs")
    ec2 = s.resource('ec2')
    iscore = TaggedInstancePool("isCore")

    for i in iscore.all:
        print(i + ":" + InstancePropertiesUtil.get_name(ec2, i))
