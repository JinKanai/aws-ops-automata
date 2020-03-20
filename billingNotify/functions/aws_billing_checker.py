import boto3
from datetime import date
import calendar


class AwsBillingChecker:
    def __init__(self):
        self.client = boto3.client("ce")
        self.costs = {}
        self.today = date.today()

    def get_cost_raw_data(self):
        start = self.get_first_day().isoformat()
        end = self.get_last_day().isoformat()
        return self.fetch_aws_api(start, end)

    def fetch_aws_api(self, start, end):
        cost = self.client.get_cost_and_usage(
            TimePeriod={'Start': start, "End": end},
            Granularity="MONTHLY", Metrics=['UnblendedCost'],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}])
        return cost

    def get_costs(self):
        billing = self.get_cost_raw_data()
        for service in billing["ResultsByTime"][0]["Groups"]:
            self.costs.update({service["Keys"][0]: float(service["Metrics"]["UnblendedCost"]["Amount"])})
        return self.costs

    def get_total_cost(self):
        total_cost = 0.0
        for cost in self.costs.values():
            total_cost += cost
        return total_cost

    def get_first_day(self):
        return self.today.replace(day=1)

    def get_last_day(self):
        last_day = calendar.monthrange(self.today.year, self.today.month)[1]
        return self.today.replace(day=last_day)


if __name__ == '__main__':
    b = AwsBillingChecker()
    print(b.get_cost_raw_data())
    for i in b.get_cost_raw_data()["ResultsByTime"][0]["Groups"]:
        print(i)
    print(b.get_costs())
    print(b.get_total_cost())
