def anagram(s1: str, s2: str) -> bool:
    new1 = sorted("".join(s1.lower().split()))
    new2 = sorted("".join(s2.lower().split()))
    return new1 == new2