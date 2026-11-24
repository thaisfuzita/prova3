def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    if not number or from_base < 2 or from_base > 36 or to_base < 2 or to_base > 36:
        return "ERROR"

    try:
        decimal = int(number, from_base)
    except ValueError:
        return "ERROR"

    if decimal == 0:
        return '0'

    if decimal < 0:
        result = "-"
        decimal *= -1

    while decimal > 0:
        result = digits[decimal % to_base] + result
        decimal = decimal // to_base

    return result