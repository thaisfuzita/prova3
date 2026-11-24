def cryptic_sorter(strings: list[str]) -> list[str]:
    ordered = strings.copy()
    for _ in range(len(ordered)):
        for i in range(len(ordered) - 1):
            if len(ordered[i]) > len(ordered[i + 1]):
                ordered[i], ordered[i + 1] = ordered[i + 1], ordered[i]
            elif len(ordered[i]) == len(ordered[i + 1]) and ordered[i].lower() > ordered[i + 1].lower():
                ordered[i], ordered[i + 1] = ordered[i + 1], ordered[i]
    return ordered
