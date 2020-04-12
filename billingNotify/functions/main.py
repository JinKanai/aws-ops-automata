import os

from aws_billing_checker import AwsBillingChecker
from fx_market_store import FxMarketStore
from slack import SlackHandler


def lambda_handler(event, context):
    ce = AwsBillingChecker()

    fx = FxMarketStore()
    fx.fetch_currency_api()

    slack = SlackHandler()

    try:
        env_name = os.environ["ENV_NAME"]
    except KeyError as e:
        env_name = "hoge"

    slack.set_pre_text("毎朝の料金通知")

    slack.set_title(
        env_name + " " + str(ce.today.month) + "月の利用料金明細（" + str(ce.today.isoformat()) + "現在）")
    slack.set_color("#f8991e")

    costs = ce.get_costs()
    message = construct_message(costs)

    total_cost = round(ce.get_total_cost(), 2)
    jpy_total_cost = "{:,d}".format(int(fx.get_jpy(total_cost)))
    # message.append({"title": "--------\n★合計金額", "value": str(total_cost) + "USD (約" + jpy_total_cost + "円)"})
    slack.set_text("★合計金額 " + str(total_cost) + "USD (約" + jpy_total_cost + "円)")

    slack.set_attachments(message)

    res = slack.post_message()
    return res


def construct_message(costs):
    message = []
    for service, cost in costs.items():
        cost = str(round(cost, 1))
        if cost != "0.0":
            d = {"title": service, "value": cost + "USD", "short": False}
            message.append(d)
    if not message:
        message = [{"title": "0.1USD以下のため明細表示省略", "value": None}]
    return message


if __name__ == "__main__":
    r = lambda_handler(None, None)
    print(r)
