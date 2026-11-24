def bracket_validator(s: str) -> bool:
    brackets = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for c in s:
        if c in brackets.keys():
            stack.append(c)
        elif c in brackets.values():
            if not stack or c != brackets[(stack[-1])]:
                return False
            else:
                stack.pop()
    if not stack:
        return True
    return False