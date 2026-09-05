import re
import json


def read_input(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


EMAIL_PATTERN = r"[a-z]+@[a-z.]+[a-z]+"
CREDIT_CARD_PATTERN = r"(\b(?:\d{4}[- ]?){3}\d{4}\b)"
URL_PATTERN = r"https?://[^\s<]*[^\s<.]"


def extract_emails(text):
    return re.findall(EMAIL_PATTERN, text)

def extract_urls(text):
    return re.findall(URL_PATTERN, text)

def extract_credit_cards(text):
    raw_matches = re.findall(CREDIT_CARD_PATTERN, text)
    valid_cards = []
    for card in raw_matches:
        if is_valid_luhn(card):
            valid_cards.append(card)
    return valid_cards


def is_valid_luhn(card_number):
    card_number = card_number.replace(" ", "").replace("-", "")
    digits = card_number[::-1]
    total = 0
    for index, digit in enumerate(digits):
        num = int(digit)
        if index % 2 == 1:
            num = num * 2
            if num > 9:
                num = num - 9
        total = total + num
    if total % 10 == 0:
        return True
    else:
        return False


def classify_alu_email(email):
    if email.endswith("@alumni.alueducation.com"):
        return "ALU Alumni"
    elif email.endswith("@si.alueducation.com"):
        return "ALU SI"
    elif email.endswith("@alueducation.com"):
        return "ALU Student"
    else:
        return "Not ALU"


def mask_credit_card(card_number):
    last_four = card_number[-4:]
    return "the card last four digits:" + last_four


def main():
    raw_text = read_input("input/raw-text.txt")
    emails = extract_emails(raw_text)
    urls = extract_urls(raw_text)
    credit_cards = extract_credit_cards(raw_text)
    masked_cards = []

    classified = {}
    for email in emails:
        category = classify_alu_email(email)
        if category not in classified:
            classified[category] = []
        classified[category].append(email)

    for card in credit_cards:
        masked_cards.append(mask_credit_card(card))
    results = {
        "emails": emails,
        "credit_cards": masked_cards,
        "urls": urls,
    }

    with open("output/sample-output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("Extraction complete. Results saved to output/sample-output.json")
    print(f"Emails found: {len(emails)}")
    print(f"Credit cards found: {len(credit_cards)}")


if __name__ == "__main__":
    main()
