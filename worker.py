from PyQt5.QtCore import QThread, pyqtSignal
from utils import parse_date, calc

class Worker(QThread):
    log = pyqtSignal(str)
    row = pyqtSignal(list)

    def __init__(self, api, nicks):
        super().__init__()
        self.api = api
        self.nicks = nicks
        self.running = True

    def run(self):
        for nick in self.nicks:
            if not self.running:
                break

            self.log.emit(f"check {nick}")

            try:
                data = self.api.search(nick)
                users = data["searchResult"]["initialMatchList"]

                exact = next(
                    (u for u in users if u["userNickData"]["nick"].lower() == nick.lower()),
                    None
                )

                if not exact:
                    continue

                dt = parse_date(exact["lastOnline"])
                if not dt:
                    continue

                r45, r60 = calc(dt)

                self.row.emit([
                    nick,
                    str(exact["userId"]),
                    r45,
                    r60
                ])

                self.msleep(200)

            except Exception as e:
                self.log.emit(str(e))
