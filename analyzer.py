import math
import string


def load_common_passwords():
    try:
        with open(
            "common_passwords.txt",
            "r",
            encoding="utf-8"
        ) as file:
            return {
                line.strip().lower()
                for line in file
            }
    except FileNotFoundError:
        return set()


def analyze_password(password):

    common_passwords = load_common_passwords()

    length = len(password)

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = 0

    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    if has_upper:
        score += 1

    if has_lower:
        score += 1

    if has_digit:
        score += 1

    if has_special:
        score += 1

    is_common = (
        password.lower()
        in common_passwords
    )

    if is_common:
        score -= 2

    charset = 0

    if has_lower:
        charset += 26

    if has_upper:
        charset += 26

    if has_digit:
        charset += 10

    if has_special:
        charset += 32

    entropy = (
        length * math.log2(charset)
        if charset > 0 else 0
    )

    suggestions = []

    if length < 12:
        suggestions.append(
            "Use at least 12 characters"
        )

    if not has_upper:
        suggestions.append(
            "Add uppercase letters"
        )

    if not has_lower:
        suggestions.append(
            "Add lowercase letters"
        )

    if not has_digit:
        suggestions.append(
            "Add numbers"
        )

    if not has_special:
        suggestions.append(
            "Add special characters"
        )

    if is_common:
        suggestions.append(
            "This password is commonly used and unsafe"
        )

    if score <= 2:
        strength = "Weak"

    elif score <= 4:
        strength = "Medium"

    else:
        strength = "Strong"

    return {
        "strength": strength,
        "entropy": round(entropy, 2),
        "upper": has_upper,
        "lower": has_lower,
        "digit": has_digit,
        "special": has_special,
        "common": is_common,
        "suggestions": suggestions
    }