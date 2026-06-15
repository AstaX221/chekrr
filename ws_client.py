import asyncio
import websockets

class WSClient:
    def __init__(self, url, recovery):
        self.url = url
        self.recovery = recovery
        self.running = True

    async def run(self):
        while self.running:
            try:
                async with websockets.connect(self.url) as ws:
                    await ws.send(f"RECOVER {self.recovery}")

                    while self.running:
                        await ws.send("PING")
                        await asyncio.sleep(20)

            except:
                await asyncio.sleep(2)
