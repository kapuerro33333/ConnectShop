import random

# ---------------- Заглушки для стабільних smoke-тестів ----------------

# Існуючий товар (очікуємо знайти в результатах пошуку)
search_text = "Smart Padlock Bluetooth"

# Неіснуючий товар (очікуємо повідомлення 'No results found')
search_text_invalid = "adrakadabra"


# ---------------- Набір значень для параметризованих тестів ----------------

SEARCH_VALUES_EXISTING = [
    "smart door lock",
    "wifi camera",
    "robot vacuum",
]

SEARCH_VALUES_NON_EXISTING = [
    "purple unicorn lamp",
    "retro mp3 cassette",
    "nonexistent gadget",
]


# ---------------- Хелпери для випадкових тестів ----------------

def get_random_existing() -> str:
    """Отримати випадковий існуючий товар"""
    return random.choice(SEARCH_VALUES_EXISTING)


def get_random_non_existing() -> str:
    """Отримати випадковий вигаданий товар"""
    return random.choice(SEARCH_VALUES_NON_EXISTING)
def get_random_search_value() -> str:
    """Зворотна сумісність: раніше тести імпортували цю функцію.
    Тепер вона делегує на get_random_existing(), щоб уникати флаків."""
    return get_random_existing()