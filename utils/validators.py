import re
from datetime import datetime

# Phone number validation: accepts international formats
def validate_phone(phone: str) -> bool:
    pattern = r'^\+?1?\d{9,15}'
    return bool(re.match(pattern, phone))

# Email validation: standard email format check
def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return bool(re.match(pattern, email))

# Amount validation: ensures positive numeric value
def validate_amount(amount: str) -> bool:
    try:
        float_amount = float(amount)
        return float_amount > 0
    except ValueError:
        return False

# Date validation: checks YYYY-MM-DD format
def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
