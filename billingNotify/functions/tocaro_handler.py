import os

from http_client import HttpClient


class TocaroHandler:

    def __init__(self):
        self.message = {
            "text": "string",
            "color": "color //info,warning,danger,success",
            "attachments": [
                {
                    "title": "string",
                    "value": "string"
                },
                {"image_url": "URL"}

            ]
        }

    def set_text(self, text):
        self.message["text"] = text

    def set_color(self, color):
        self.message["color"] = color

    def set_attachments(self, contents):
        self.message["attachments"] = contents

    def send2tocaro(self):
        tocaro_url = os.environ["MESSENGER_URL"]
        headers = {"Content-type": "application/json"}
        body = HttpClient.post(tocaro_url, self.message, headers)
        return body


if __name__ == "__main__":
    t = TocaroHandler()
    t.set_text("test-death")
    t.set_color("danger")
    print(t.send2tocaro())
