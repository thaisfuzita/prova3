def string_permutation_checker(s1: str, s2: str) -> bool:
    new1 = sorted(s1)
    new2 = sorted(s2)
    return new1 == new2