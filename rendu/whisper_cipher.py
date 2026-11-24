def whisper_cipher(text: str, shift: int) -> str:
    alpha_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alpha_lower = "abcdefghijklmnopqrstuvwxyz"
    result = ""

    for c in text:
        if c.isupper():
            i = alpha_upper.find(c)
            result += alpha_upper[(i + shift) % 26]
        elif c.islower():
            i = alpha_lower.find(c)
            result += alpha_lower[(i + shift) % 26]
        else:
            result += c

    return result