import os

from http_client import HttpClient


class PostkunBase:

    def __init__(self):
        self.message = {}

    def post_message(self):
        try:
            url = os.environ["MESSENGER_URL"]
        except KeyError as e:
            print("environment value {0} is not found.".format(e))
            return False
        headers = {"Content-type": "application/json"}
        body = HttpClient.post(url, self.message, headers)
        return body
