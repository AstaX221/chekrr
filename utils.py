import random
from datetime import datetime, timedelta

CLUSTERS = {
    "power": ["сила", "мощь", "титан", "гром", "энергия"],
    "war": ["воин", "берсерк", "рыцарь", "гладиатор"],
    "leadership": ["лидер", "главный", "вождь", "король"],
    "nation": ["россия", "русский", "держава", "империя"],
    "dark": ["смерть", "хаос", "тьма", "страх"]
}

def generate_nicks(n=80):
    keys = list(CLUSTERS.keys())
    out = set()

    while len(out) < n:
        out.add(random.choice(CLUSTERS[random.choice(keys)]))

    return list(out)


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
        return datetime(now.year, MONTHS[parts[1]], int(parts[0]))
    except:
        return None


def calc(dt):
    return (
        (dt + timedelta(days=45)).strftime("%d.%m.%Y"),
        (dt + timedelta(days=60)).strftime("%d.%m.%Y")
    )
