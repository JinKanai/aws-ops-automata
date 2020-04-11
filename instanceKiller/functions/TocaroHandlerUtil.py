import urllib.request
import json
from InstancePropertiesUtil import InstancePropertiesUtil
import boto3
import os


class TocaroHandlerUtil:
    @classmethod
    def send2tocaro(cls, *args):
        tocaro_url = os.environ['TOCARO_URL']
        # テスト用
        #tocaro_url = 'https://hooks.tocaro.im/integrations/inbound_webhook/imvshz6xtd79nmti117moogasvdewh1y'

        headers = {'Content-type': 'application/json'}

        req = urllib.request.Request(tocaro_url, json.dumps(cls.make_violation_messages(args)).encode(), headers)
        with urllib.request.urlopen(req) as res:
            body = res.read()

        return body

    @classmethod
    def make_violation_messages(cls, violation_cases):
        s = boto3.Session()
        ec2 = s.resource('ec2')

        messages = {
            'text': '本日の違反インスタンス一覧', 'color': 'danger', 'attachments': []
        }
        for violation_case in violation_cases:
            messages['attachments'].append({'title': violation_case['case_name']})
            if violation_case['instances']:
                item = ""
                for instance_id in violation_case['instances']:
                    owner = InstancePropertiesUtil.get_owner(ec2, instance_id)
                    if not owner:
                        owner = '所有者不明'
                    item += instance_id + ' : ' + owner + '\r\n'
                messages['attachments'].append({'value': item})
            else:
                messages['attachments'].append({'value': 'なし\r\n'})
        return messages

