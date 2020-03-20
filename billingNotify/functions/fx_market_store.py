from http_client import HttpClient


class FxMarketStore:
    def __init__(self):
        self.quotes = {}
        self.jpy_rate = 0.0

    def fetch_currency_api(self):
        url = "https://www.gaitameonline.com/rateaj/getrate"
        headers = {
            "User-Agent": "python"
        }
        self.quotes = HttpClient.get(url, headers)
        self._get_jpy_rate()

    def _get_jpy_rate(self):
        for quote in self.quotes["quotes"]:
            if quote["currencyPairCode"] == "USDJPY":
                self.jpy_rate = float(quote["ask"])
                break

    def get_jpy(self, usd):
        return self.jpy_rate * usd


def test_rate():
    import json
    with open("./tests/gaitame.json", "r") as f:
        sample_data = json.load(f)
    f = FxMarketStore()
    f.quotes = sample_data
    f._get_jpy_rate()
    print(f.get_jpy(1.5))


if __name__ == '__main__':
    test_rate()
