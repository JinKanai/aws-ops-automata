from base import PostkunBase


class SlackHandler(PostkunBase):

    def __init__(self):
        self.message = {
            "channel": "hoge",
            "text": "hoge",
            "attachments": [
                {
                    # "fallback": "FALLBACK TEXT.",
                    # "color": "#2eb886",
                    # "pretext": "",
                    # "author_name": "AWS BillingNotify",
                    # "author_icon": "http://flickr.com/icons/bobby.jpg",
                    # "title": "AWS x月の利用料金",
                    # "title_link": "https://api.slack.com/",
                    # "text": "本日までの累計：20$ (約2000円)",
                    # "fields": [
                    #    {
                    #        "title": "EC2",
                    #        "value": "12 USD",
                    #        "short": False
                    #    },
                    #    {
                    #        "title": "Lambda",
                    #        "value": "0.11 USD",
                    #        "short": False
                    #    }
                    # ],
                    # "image_url": "http://my-website.com/path/to/image.jpg",
                    # "thumb_url": "http://example.com/path/to/thumb.png",
                    # "footer": "Slack API",
                    # "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                    # "ts": 1234567898
                }
            ]
        }

    def set_pre_text(self, text):
        self.message["text"] = text

    def set_title(self, title):
        self.message["attachments"][0]["title"] = title

    def set_text(self, text):
        self.message["attachments"][0]["text"] = text

    def set_color(self, color):
        self.message["attachments"][0]["color"] = color

    def set_attachments(self, contents):
        self.message["attachments"][0]["fields"] = contents


if __name__ == "__main__":
    t = SlackHandler()
    t.set_title("AWS 4月の利用料金")
    t.set_text("料金通知")
    t.set_color("#f8991e")
    print(t.post_message())
