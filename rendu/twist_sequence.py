def twist_sequence(arr: list[int], k: int) -> list[int]:
    if k == 0 or not arr:
        return arr
    k = k % len(arr)
    result = arr[len(arr) - k:] + arr[:len(arr) - k]
    return result