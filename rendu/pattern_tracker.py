def pattern_tracker(text: str) -> int:
    pairs = 0
    for i in range(len(text) - 1):
        if text[i].isdigit() and text[i + 1].isdigit() and int(text[i]) + 1 == int(text[i + 1]):
            pairs += 1
    return pairs