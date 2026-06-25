import data_processor
import random

KEYWORDS_MAP = {
    "universam": "food",
    "abrikos": "food",
    "syr bor": "food",
    "cafe": "food",
    "ekovoda": "food",
    "firmennyy": "food",
    "magazin": "food",
    "supermarket": "food",
    "spar": "food",
    "ifood": "food",
    "yarche": "food",
    "lenta": "food",
    "bezumno": "food",
    "shaurma": "food",
    "krasnoe beloe": "food",
    "mariya ra": "food",

    "yandex go": "transport",
    "tomsknefteproduct": "transport",
    "ждперевозок": "transport",
    "rnazkrosneft": "transport",

    "apteka": "health",
    "aloe": "health",

    "dns": "others",
    "cvety": "others",
    "mbank yota": "others",
    "платазаобслуживание": "others"
}

def assign_category(text):
    words = text.split()
    for word in words:
        if word in KEYWORDS_MAP:
            return KEYWORDS_MAP[word]
        else:
            return "others"