import aiohttp

class Engine:
    def __init__(self):
        self.user_id = ""
        self.password = ""

    async def search(self, nick):
        url = "https://galaxy.mobstudio.ru/services/"

        params = {
            "userID": self.user_id,
            "password": self.password
        }

        data = {
            "a": "search_ajax",
            "type": "1",
            "search_value": nick,
            "ajax": "1"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params, data=data, timeout=10) as r:
                return await r.json()
