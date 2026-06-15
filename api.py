import requests

class API:
    def __init__(self):
        self.user_id = ""
        self.password = ""

    def search(self, nick):
        r = requests.post(
            "https://galaxy.mobstudio.ru/services/",
            params={"userID": self.user_id, "password": self.password},
            data={
                "a": "search_ajax",
                "type": "1",
                "search_value": nick,
                "ajax": "1"
            },
            timeout=10
        )
        return r.json()
