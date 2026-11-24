def echo_validator(text: str) -> bool:
    new = ""
    for c in text:
        if c.isalpha():
            new += c.lower()
    return new == new[::-1]