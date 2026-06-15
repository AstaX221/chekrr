import random
from datetime import datetime, timedelta

CLUSTERS = {
    "power": ["сила", "мощь", "титан", "гром"],
    "war": ["воин", "берсерк", "рыцарь"],
    "leadership": ["лидер", "главный", "король"],
    "nation": ["россия", "русский", "империя"],
    "dark": ["смерть", "хаос", "тьма"]
}

def gen_nicks(n=80):
    out = set()
    keys = list(CLUSTERS.keys())

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

    t = text.lower()
    now = datetime.now()

    if "вчера" in t:
        return now - timedelta(days=1)
    if "сегодня" in t:
        return now

    try:
        p = t.split()
        return datetime(now.year, MONTHS[p[1]], int(p[0]))
    except:
        return None


def calc(dt):
    return (
        (dt + timedelta(days=45)).strftime("%d.%m.%Y"),
        (dt + timedelta(days=60)).strftime("%d.%m.%Y")
    )
