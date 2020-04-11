import boto3
from InstancesRuleViolationCollection import InstancesRuleViolationCollection
from TaggedInstancePool import TaggedInstancePool
from TocaroHandlerUtil import TocaroHandlerUtil


def lambda_handler(event, context):
    s = boto3.Session()
    ec2 = s.resource('ec2')
    in_violation = InstancesRuleViolationCollection(ec2)

    client_ec2 = s.client('ec2')
    iscore = TaggedInstancePool(client_ec2, 'isCore')

    days_passed = {'case_name': '最終起動から３日以上経過したインスタンス',
                   'instances': [i for i in in_violation.get_days_passed_instances(iscore.have_nots)]}

    over_spec = {'case_name': 't2.nano/t2.micro以上のサイズを使用しているインスタンス',
                 'instances': [i for i in in_violation.get_overspec_instances(iscore.have_nots)]}

    unnamed = {'case_name': 'Nameタグに名称を設定していないインスタンス',
               'instances': [i for i in in_violation.get_unnamed_instances(iscore.have_nots)]}

    owner_unknown = {'case_name': 'Ownerタグに所有者を設定していないインスタンス',
                     'instances': [i for i in in_violation.get_owner_unknown_instances(iscore.have_nots)]}

    unprotected = {'case_name': 'TDAWS_InternalDesignatedセキュリティグループを設定していないインスタンス',
                   'instances': [i for i in in_violation.get_unprotected_instances(iscore.have_nots)]}

    TocaroHandlerUtil.send2tocaro(days_passed, over_spec, unnamed, owner_unknown, unprotected)
    return days_passed, over_spec, unnamed, owner_unknown, unprotected


if __name__ == '__main__':
    print(lambda_handler(None, None))

