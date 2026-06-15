import sys
import random
import time
import requests
import sqlite3

from datetime import datetime, timedelta

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit
)
from PyQt5.QtCore import QThread, pyqtSignal

# =========================
# 🔹 НИКИ
# =========================

CLUSTERS = {
    "power": ["сила", "мощь", "титан", "гром", "энергия"],
    "war": ["воин", "берсерк", "рыцарь", "гладиатор"],
    "leadership": ["лидер", "главный", "вождь", "король"],
    "nation": ["россия", "русский", "держава", "империя"],
    "dark": ["смерть", "хаос", "тьма", "страх"]
}

def generate_nicks(n=50):
    keys = list(CLUSTERS.keys())
    out = []
    while len(out) < n:
        w = random.choice(CLUSTERS[random.choice(keys)])
        if w not in out:
            out.append(w)
    return out


# =========================
# 🔹 БД
# =========================

conn = sqlite3.connect("nicks.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS nicks (
    nick TEXT PRIMARY KEY,
    user_id INTEGER,
    last_online TEXT,
    r45 TEXT,
    r60 TEXT
)
""")
conn.commit()


# =========================
# 🔹 ДАТЫ
# =========================

MONTHS = {
    "января":1,"февраля":2,"марта":3,"апреля":4,"мая":5,"июня":6,
    "июля":7,"августа":8,"сентября":9,"октября":10,"ноября":11,"декабря":12
}

def parse_date(text):
    if not text:
        return None

    text = text.lower()
    now = datetime.now()

    if "сегодня" in text:
        return now

    if "вчера" in text:
        return now - timedelta(days=1)

    try:
        parts = text.split()
        day = int(parts[0])
        month = MONTHS.get(parts[1], 1)
        return datetime(now.year, month, day)
    except:
        return None


def calc(dt):
    return (
        (dt + timedelta(days=45)).strftime("%d.%m.%Y"),
        (dt + timedelta(days=60)).strftime("%d.%m.%Y")
    )


# =========================
# 🔹 API
# =========================

class API:
    def __init__(self):
        self.user_id = ""
        self.password = ""

    def search(self, nick):
        r = requests.post(
            "https://galaxy.mobstudio.ru/services/",
            params={
                "userID": self.user_id,
                "password": self.password
            },
            data={
                "a": "search_ajax",
                "type": "1",
                "search_value": nick,
                "ajax": "1"
            }
        )
        return r.json()


# =========================
# 🔹 WORKER (поток)
# =========================

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

            try:
                self.log.emit(f"Checking {nick}")

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

                cur.execute("""
                    INSERT OR REPLACE INTO nicks VALUES (?,?,?,?,?)
                """, (
                    nick,
                    exact["userId"],
                    exact["lastOnline"],
                    r45,
                    r60
                ))
                conn.commit()

                time.sleep(1)

            except Exception as e:
                self.log.emit(str(e))


# =========================
# 🔹 GUI
# =========================

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.api = API()

        self.setWindowTitle("Galaxy Tool v4")
        self.setGeometry(300, 200, 800, 500)

        layout = QVBoxLayout()

        self.user = QLineEdit()
        self.user.setPlaceholderText("USER ID")

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("PASSWORD")

        self.btn = QPushButton("START")

        self.log = QLabel("LOG")

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Nick", "UserID", "+45", "+60"]
        )

        layout.addWidget(self.user)
        layout.addWidget(self.pwd)
        layout.addWidget(self.btn)
        layout.addWidget(self.log)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.btn.clicked.connect(self.start)

    def add_row(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)

        for i, val in enumerate(data):
            self.table.setItem(row, i, QTableWidgetItem(val))

    def start(self):
        self.api.user_id = self.user.text()
        self.api.password = self.pwd.text()

        nicks = generate_nicks(50)

        self.worker = Worker(self.api, nicks)
        self.worker.log.connect(self.log.setText)
        self.worker.row.connect(self.add_row)
        self.worker.start()


# =========================
# 🔹 RUN
# =========================

app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
