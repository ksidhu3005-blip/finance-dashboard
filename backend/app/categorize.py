"""
Auto-categorization logic.

Kept in its own file (separate from crud.py) because this is the one piece
of business logic that's genuinely interesting on its own — it's a pure
function with no database or HTTP dependency, so it's easy to test in
isolation.
"""


def categorize(description: str, rules: list[dict]) -> str:
    """
    Check a transaction description against a list of keyword->category
    rules. Case-insensitive. Falls back to 'Uncategorized' if nothing matches.
    """
    desc = description.lower()
    for rule in rules:
        if rule["keyword"].lower() in desc:
            return rule["category"]
    return "Uncategorized"


# Starter rules seeded into the database on first run so the app looks
# useful immediately instead of showing "Uncategorized" for everything.
DEFAULT_RULES = [
    {"keyword": "rent", "category": "Housing"},
    {"keyword": "uber", "category": "Transport"},
    {"keyword": "careem", "category": "Transport"},
    {"keyword": "amazon", "category": "Shopping"},
    {"keyword": "netflix", "category": "Subscriptions"},
    {"keyword": "spotify", "category": "Subscriptions"},
    {"keyword": "carrefour", "category": "Groceries"},
    {"keyword": "lulu", "category": "Groceries"},
    {"keyword": "grocery", "category": "Groceries"},
    {"keyword": "salary", "category": "Income"},
    {"keyword": "electricity", "category": "Utilities"},
    {"keyword": "water bill", "category": "Utilities"},
    {"keyword": "du telecom", "category": "Utilities"},
    {"keyword": "etisalat", "category": "Utilities"},
    {"keyword": "restaurant", "category": "Dining"},
    {"keyword": "starbucks", "category": "Dining"},
]