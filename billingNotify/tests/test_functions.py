import unittest
from unittest.mock import Mock, patch
import sys

sys.path.append("../functions")
from aws_billing_checker import AwsBillingChecker
import main


class TestFunctions(unittest.TestCase):
    def setUp(self):
        import json
        with open("./cost_and_usage.json", "r") as f:
            self.cost_and_usage = json.load(f)
        self.target = AwsBillingChecker()
        self.expected_costs = {
            "AWS CloudTrail": 0.0, "AWS Config": 1.41, "AWS Cost Explorer": 0.38, "AWS Glue": 0.0,
            "AWS Key Management Service": 0.001101, "AWS Lambda": 0.2551512218, "Amazon DynamoDB": 1.9152456214,
            "EC2 - Other": 42.8136991768, "Amazon Elastic Compute Cloud - Compute": 77.4074750681,
            "Amazon Elasticsearch Service": 49.1370047456, "Amazon Simple Notification Service": 0.0051707872,
            "Amazon Simple Queue Service": 0.0045912068, "Amazon Simple Storage Service": 0.1060170327,
            "AmazonCloudWatch": 6.0574654633, "Tax": 18.03
        }

    @patch("aws_billing_checker.AwsBillingChecker.get_cost_raw_data")
    def test_get_costs(self, mocked):
        mocked.return_value = self.cost_and_usage
        result = self.target.get_costs()
        self.assertDictEqual(result, self.expected_costs)

    @unittest.skip("in case don't output about zero cost")
    def test_construct_message(self):
        expected_message = [{"title": "AWS CloudTrail", "value": "0.0USD"}, {"title": "AWS Config", "value": "1.4USD"},
                            {"title": "AWS Cost Explorer", "value": "0.4USD"}, {"title": "AWS Glue", "value": "0.0USD"},
                            {"title": "AWS Key Management Service", "value": "0.0USD"},
                            {"title": "AWS Lambda", "value": "0.3USD"}, {"title": "Amazon DynamoDB", "value": "1.9USD"},
                            {"title": "EC2 - Other", "value": "42.8USD"},
                            {"title": "Amazon Elastic Compute Cloud - Compute", "value": "77.4USD"},
                            {"title": "Amazon Elasticsearch Service", "value": "49.1USD"},
                            {"title": "Amazon Simple Notification Service", "value": "0.0USD"},
                            {"title": "Amazon Simple Queue Service", "value": "0.0USD"},
                            {"title": "Amazon Simple Storage Service", "value": "0.1USD"},
                            {"title": "AmazonCloudWatch", "value": "6.1USD"}, {"title": "Tax", "value": "18.0USD"}]
        result = main.construct_message(self.expected_costs)
        self.assertListEqual(result, expected_message)

    def test_construct_message_without_zero(self):
        expected_message = [{"title": "AWS Config", "value": "1.4USD"},
                            {"title": "AWS Cost Explorer", "value": "0.4USD"},
                            {"title": "AWS Lambda", "value": "0.3USD"}, {"title": "Amazon DynamoDB", "value": "1.9USD"},
                            {"title": "EC2 - Other", "value": "42.8USD"},
                            {"title": "Amazon Elastic Compute Cloud - Compute", "value": "77.4USD"},
                            {"title": "Amazon Elasticsearch Service", "value": "49.1USD"},
                            {"title": "Amazon Simple Storage Service", "value": "0.1USD"},
                            {"title": "AmazonCloudWatch", "value": "6.1USD"}, {"title": "Tax", "value": "18.0USD"}]
        result = main.construct_message(self.expected_costs)
        self.assertListEqual(result, expected_message)


if __name__ == "__main__":
    unittest.main()
