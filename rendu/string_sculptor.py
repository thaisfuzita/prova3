def string_sculptor(text: str) -> str:
    i = 0
    result = ""
    for c in text.lower():
        if c.isalpha():
            if i % 2 == 0:
                result += c
            else:
                result += c.upper()
            i += 1
        else:
            result += c
    return result
