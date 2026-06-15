import sys
import asyncio

from PyQt5.QtWidgets import *
from qasync import QEventLoop, asyncSlot

from engine import Engine
from ws_client import WSClient
from utils import gen_nicks, parse_date, calc


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.engine = Engine()

        self.setWindowTitle("Galaxy Tool V6")
        self.resize(900, 600)

        layout = QVBoxLayout()

        self.uid = QLineEdit()
        self.pwd = QLineEdit()
        self.rc = QLineEdit()

        self.btn = QPushButton("START")

        self.log = QLabel("LOG")

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nick","ID","+45","+60"])

        layout.addWidget(self.uid)
        layout.addWidget(self.pwd)
        layout.addWidget(self.rc)
        layout.addWidget(self.btn)
        layout.addWidget(self.log)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.btn.clicked.connect(self.start)

    @asyncSlot()
    async def start(self):
        self.engine.user_id = self.uid.text()
        self.engine.password = self.pwd.text()

        # WS
        self.ws = WSClient(
            "wss://galaxy.mobstudio.ru/websocket",
            self.rc.text()
        )
        asyncio.create_task(self.ws.run())

        # SEARCH LOOP (ASYNC)
        nicks = gen_nicks(80)

        for nick in nicks:
            self.log.setText(f"checking {nick}")

            try:
                data = await self.engine.search(nick)

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

                row = self.table.rowCount()
                self.table.insertRow(row)

                self.table.setItem(row,0,QTableWidgetItem(nick))
                self.table.setItem(row,1,QTableWidgetItem(str(exact["userId"])))
                self.table.setItem(row,2,QTableWidgetItem(r45))
                self.table.setItem(row,3,QTableWidgetItem(r60))

            except Exception as e:
                self.log.setText(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = App()
    window.show()

    with loop:
        loop.run_forever()
