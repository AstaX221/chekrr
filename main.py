import sys
import sqlite3
from PyQt5.QtWidgets import *

from api import API
from ws_client import WSClient
from worker import Worker
from utils import generate_nicks


conn = sqlite3.connect("nicks.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS nicks (
    nick TEXT PRIMARY KEY,
    user_id TEXT,
    r45 TEXT,
    r60 TEXT
)
""")
conn.commit()


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.api = API()

        self.setWindowTitle("Galaxy Tool V5")
        self.setGeometry(200, 200, 900, 600)

        layout = QVBoxLayout()

        self.uid = QLineEdit()
        self.uid.setPlaceholderText("USER ID")

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("PASSWORD")

        self.rc = QLineEdit()
        self.rc.setPlaceholderText("RECOVERY CODE")

        self.start = QPushButton("START")

        self.log = QLabel("LOG")

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nick","ID","+45","+60"])

        layout.addWidget(self.uid)
        layout.addWidget(self.pwd)
        layout.addWidget(self.rc)
        layout.addWidget(self.start)
        layout.addWidget(self.log)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.start.clicked.connect(self.run_all)

    def add_row(self, data):
        r = self.table.rowCount()
        self.table.insertRow(r)
        for i, v in enumerate(data):
            self.table.setItem(r, i, QTableWidgetItem(v))

    def run_all(self):
        self.api.user_id = self.uid.text()
        self.api.password = self.pwd.text()

        # WS
        self.ws = WSClient(
            "wss://galaxy.mobstudio.ru/websocket",
            self.rc.text()
        )
        self.ws.start()

        # Worker
        self.worker = Worker(self.api, generate_nicks(80))
        self.worker.log.connect(self.log.setText)
        self.worker.row.connect(self.add_row)
        self.worker.start()


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
