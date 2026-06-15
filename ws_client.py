import websocket
import threading
import time

class WSClient:
    def __init__(self, url, recovery_code):
        self.url = url
        self.recovery_code = recovery_code
        self.ws = None
        self.running = True

    def on_open(self, ws):
        ws.send(f"RECOVER {self.recovery_code}")

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open
        )

        threading.Thread(target=self._run, daemon=True).start()
        threading.Thread(target=self._ping, daemon=True).start()

    def _run(self):
        self.ws.run_forever()

    def _ping(self):
        while self.running:
            try:
                self.ws.send("PING")
            except:
                pass
            time.sleep(20)
