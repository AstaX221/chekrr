import aiohttp

class Engine:
    def __init__(self):
        self.user_id = ""
        self.password = ""

    async def search(self, nick):
        url = "https://galaxy.mobstudio.ru/services/"

        data = {
            "a": "search_ajax",
            "type": "1",
            "search_value": nick,
            "ajax": "1"
        }

        params = {
            "userID": self.user_id,
            "password": self.password
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params, data=data) as resp:
                return await resp.json()
