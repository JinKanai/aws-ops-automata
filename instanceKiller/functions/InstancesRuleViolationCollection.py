import boto3
from TaggedInstancePool import TaggedInstancePool
from datetime import datetime, timezone
from InstancePropertiesUtil import InstancePropertiesUtil


class InstancesRuleViolationCollection:

    def __init__(self, session):
        self.old_instances = []
        self.unprotected_instances = []
        self.overspec_instances = []
        self.owner_unknown_instances = []
        self.unnamed_instances = []
        self.ec2 = session

    def get_old_instances(self, target_candidates, days=3):
        # 現在時刻をawareで取得
        now = datetime.now(timezone.utc)
        for instance_id in target_candidates:
            # インスタンスが最後に起動された時刻をawareで取得
            lt = InstancePropertiesUtil.get_launch_date(self.ec2, instance_id)
            if (now - lt).days > days:
                self.old_instances.append(instance_id)
        return self.old_instances

    def get_unprotected_instances(self, target_candidates):
        for instance_id in target_candidates:
            sgs = self.ec2.Instance(instance_id).security_groups
            for sg in sgs:
                if sg["GroupName"] != "TDAWS_InternalDesignated":
                    self.unprotected_instances.append(instance_id)
                    break
        return self.unprotected_instances

    def get_overspec_instances(self, target_candidates):
        for instance_id in target_candidates:
            spec = self.ec2.Instance(instance_id).instance_type
            if spec != "t2.micro" and spec != "t2.nano":
                self.overspec_instances.append(instance_id)
        return self.overspec_instances

    def get_owner_unknown_instances(self, target_candidates):
        for instance_id in target_candidates:
            if not InstancePropertiesUtil.get_owner(self.ec2, instance_id):
                self.owner_unknown_instances.append(instance_id)
        return self.owner_unknown_instances

    def get_unnamed_instances(self, target_candidates):
        for instance_id in target_candidates:
            if not InstancePropertiesUtil.get_name(self.ec2, instance_id):
                self.unnamed_instances.append(instance_id)
        return self.unnamed_instances


if __name__ == '__main__':
    s = boto3.Session(profile_name="ctcs")
    ec2 = s.resource('ec2')
    c = InstancesRuleViolationCollection(ec2)
    iscore = TaggedInstancePool("isCore")

    print("old")
    for i in c.get_old_instances(iscore.havenots):
        print(i + ": " + InstancePropertiesUtil.get_name(ec2, i))
        print("last_launch_time: {}".format(InstancePropertiesUtil.get_launch_date(ec2, i)))
    print()

    print("unprotected")
    for i in c.get_unprotected_instances(iscore.havenots):
        print(i + ": " + InstancePropertiesUtil.get_name(ec2, i))
    print()

    print("overspec")
    for i in c.get_overspec_instances(iscore.havenots):
        print(i + ": " + InstancePropertiesUtil.get_name(ec2, i))
    print()

    print("owner unknown")
    for i in c.get_owner_unknown_instances(iscore.havenots):
        print(i + ": " + InstancePropertiesUtil.get_name(ec2, i))
    print()

    print("unnamed")
    for i in c.get_unnamed_instances(iscore.havenots):
        print(i + ": " + InstancePropertiesUtil.get_name(ec2, i))
    print()
