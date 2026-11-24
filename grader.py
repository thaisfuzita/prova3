#!/usr/bin/env python3
"""Simulado da prova rank 3.

Uso:
  python3 grader.py                 corrige as 14 questoes (OK / KO)
  python3 grader.py anagram         corrige so uma questao
  python3 grader.py -d anagram      mostra o primeiro teste que falhou
  python3 grader.py --prova         modo prova: nivel por nivel, questao sorteada

Suas respostas ficam em rendu/<nome_da_funcao>.py
"""
import ast
import base64
import copy
import json
import os
import random
import string
import subprocess
import sys
import time
import types
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
RENDU = os.path.join(HERE, 'rendu')
STATE = os.path.join(HERE, '.prova_estado.json')
TIMEOUT = 10

_REFS = "eJydVltv2zYUfs+v4B4GUqvjxu7iLEL9kLVpl92yZesuFQSBpmibsERqJBW7Dfrfd0hKliV7QDE92Lycy3e+c5GWWpWIqaLgzAolDRJlpbRFr1QtLddnZ2c5X6KFpmzDbfZIC5FTqzQxUXyG4Kmo0AbN0ROOcIwwwSOEU7dK3OqTWz3hT17UWJBLUr9eKo0YEhKZYMY9YhmOMEmecHccVMe0qrjMCYv2F7xoNTyIvgZcSWWdT/BkbHI+SdEX8yCZsLQv7B7Nba0lekMLw4e+K1WR4LeRCqYbcpj+UFnBMgO8cWDGaiFXLT+PEHNBy0VO0S5Gpi5JiJFyoeqb27v7d7gjY9dz4u3lrb0R2vAP884UKbgku2iEduNCbcEvLB/hIIoaWJyt1UHCLN/ZBpPPA2vVOvdOxGdhLAwtqjUlUXoICPTmyCZxDGQ2TkqhtdJZSQHkjoS/xkujlGi1DSreEeycqyDZWlmLnMuKmJIWxQgtxKoxIQDoRb9e4LJXMQK9RI4JrxshKnPkl4lIHVo2qAr0bI4mh/CEk+oMNICE9JmcjJCZNlhU7WjDeFC+k+P6NVMPg/kqgT1o9lE4U4CDHeKAM/D9+u6tc3Ixmb74+nJ29c31zbevXt++efvd3fc//PjTz/e//Prw2+/v/vjzr7/f4waqrMsF19mCGp4xJR+5L8JwOkJLaG9/N0JW+UVLbegPMkUv552U27yYefj+otEJx5FrJacUjHcxNSHg24eH+4dAkDzO3FDL09VQBHEn8R7FoDtPmG9dSPTVAfhnzs5YyJzv2jnhwnQZvjhGe4GP87pdi4Ij2QmHWwdPoi9bOlLw5PLVIXn+fM/VcVJdlipqIS0ys36Q9rqx7XYYDRPPFoUWcKR8FJWXG/nGTCZxGvV4CeFRaNZcrIQlofoXgz2UMllEjgO3ohFgn7RlTiVdaVr2C33ZTSwTt+8BcmJcmJBCmKoY4d7kWoJF7xIW09aZWdNcbbOS6xUnhTAWnLq/6YCHMPW8AGANEq0JPwqziuuyttS9rzK25p7QXgiNqRZ7A2a/HdozrC6qwYzslcXmuJqdaL+Wu6F5utv3BILwBopp6usS3mJQuWxcw+tNk36CN920co+T/NxB4qKzW+AuM/yfmkvGCdUwDzb99oezo8Zo3tAAMQxGkOklF/bJ+SZ2TeCW8fkmDSH5SPxRO9ehnQyElTFRrZuihyytxfIky//NLabYjSDmfvBHfJqEtSZEafeFgM7R9RXAC54c1TPYXV8NPh3wzYHV959jdXZ5ZHV2Gf2PBP0LcT2YvQ=="
SUBJECTS = json.loads(zlib.decompress(base64.b64decode("eJydV01v3DYQ/SvEXiwD60XstAXiQwHXTYpcksJJEaBRsOBKsyvWEqmSlNeLIP+9b4b6Wsc1jBySlUbkcObNmzf018XG6+KW4vpO16bU0fnFpVqUtFXffcjCpQrRn6qzX9XGufoyt7n95E0kpdW2s0U0zqpY6aiKiorboMwWrzR4wrvFSrgwdqe0JyWuV+zmajCbkKy8l+7IH5RryfKX3ouqdICXRseiYnNRuzD7nGOtHFo476mIyvmSfDqjrt2eyjGcS5WdLtXnL0v19dtiqRaFP7TRFOvgfKQRhmNrlsLE3tqE+BlvXwSP8e0JUNgDh85rldv2GcNSINaSc4hONV0dTVsjfvbhjYbD85X605tGAwz2cal+Owxw1WR3sVJZqDg8+N0aH+Jpbi9W6gMVzpbTrqsP12/fJjyWiu4LaiP2R5wSpBqFa1r8lqrQgc6MDWSDieaO6kNulVLZ1vkxaI5fN9QHgANfrtRH8tEcRWm7ZkOeF98B+jqoTIeCLCe7VOJu8qG0LfF4bwpd1wdF/3a6ht+fVuo1P44n701dK922pL3qay1eJDGlw2A0tu2igC3Vf+P8xpQl2bEqTGdGrWQayDp+zU6ZC1RU7vuWOLZmke7jD7SEnnFdqxbubOldQ0twd2edfAqtLigIJFyNpXIWmKCewUiWdVvpDYGX8KvBZy5ibhnRxH2upAnOrjiZxnjv/Bot4839kMuRMUs/PavlP2Pjlxm3J5vk+Adowc188btKW1U20Jp/AxD1FDvPayzth0X7ikA00kWlvNsj34Bl6PJApURaITvbDiGmtyw0IITgvFQbs/tBEeoxPxFvJwn70G0CeEa2oNwi9BO4P1mpq/kH1ZC2WAzSTVBznoOniYqyfRSgiZQIG0y0Dv8IVQ0oTV9MKrrUYKDomyF4hCYdOPafQAPsJ1GSlyyc96iEiwkU/D6BSSpKmDi4N+g84cyUnKxMaUk2G4c1ffstZYfr2FULAkojrdT1tJulRKPRyqERBYPc4vHwoG9FrHrPkmTSi/UG6a+BD5gxS/rRj1my9kBs0Uey4JIhWkJQp7dnoNN7ZXh65WKH6D3MMLhhfdYoYyUD5UPXttAL+RLSwgte8fIXnFbUXeDK5fYv7CvNzsDri7NXvcgl0b06+1tEEIrSwcX5i7OXP2PHTWqcfPH65ub9Tb6QNcb2Y5FVLQhYrWY3dh1lno0wPTA/UCkA8SQAnY1BajOTbjl4RteUDw4yLDqzoc6tk1bztyRXEAN2EvfArvwHqmbjgEdSA+kVGVW5TY7RAHQPNqFJGPqdJ42MOMIZbVZ8aXgFbIapDnKpF7z33fuPeJziELC01TuvmwGk/vXxFnq+riCpcYoz7ZPXgNg+MtubLgipogZIQ0qjNgw0GFtQrJh1Fm11mE8DlgNhThoLklCodOn264b8joas5jbR4/Ne0Vm404y7mFkmdee3JzIWhyGlKxMziTyTyUmJZtYUnICybsk3XdTsaC2oTSz9/xU/VJOSAGVjLD1al9kpQkYZQEMfXzO4k9aqTxUOEKAF8pbP6WRvag++YnjadTV0bBJNOHrdtPHw3HNnKIWiq9vZLeOB+UEDP61gaHoboBfNTOK5M2qWBATCl0wWe87ZbXP76EVCLhtI6J2zZ48v8NQwpXE0enKHyjNSnDH3nqA0yj+f0R/Os82WdJ/ao1f/xw4AkV1Xo6fRJGhun65Ak1AoSO9gpVgImHEP8q2HqT1geWzNtPdHHXE7TYbn9IF3KKZcy5Cs1weWe47Km10VGedb1brQz0QIOS9nyGff022CN9Ua2d8qqqkhFt3G3dHgENPEpk7aVyYg13Vh2mrqnmPrxBD0TGW28dnzTpSVqXKtKTCfxR9HKn7SXxhJpVjmczujlNqlO2DD5X6SLX01H5Kmp4GcBEZaLrelnZYRkyVzTdt4ulp8+w/CwkVk")).decode())

LEVELS = [
    ['bracket_validator', 'cryptic_sorter'],
    ['echo_validator', 'mirror_matrix'],
    ['hidenp', 'inter', 'number_base_converter', 'pattern_tracker'],
    ['anagram', 'shadow_merge', 'string_permutation_checker'],
    ['string_sculptor', 'twist_sequence'],
    ['whisper_cipher'],
]


def _refs():
    mod = types.ModuleType('refs')
    exec(zlib.decompress(base64.b64decode(_REFS)).decode(), mod.__dict__)
    return mod


# ---------------------------------------------------------------- testes
R = random.Random()


def rs(chars, lo=0, hi=12):
    return ''.join(R.choice(chars) for _ in range(R.randint(lo, hi)))


def t_bracket_validator():
    fixed = ['', '()', '([]{})', '([)]', '((', ')', '{[()()]}', '}{', 'a(b)c',
             '(]', '[', ']', '(((())))', '([{}])[]', 'x{y[z]}', '{(})']
    return [(s,) for s in fixed] + [(rs('()[]{}a ', 0, 10),) for _ in range(400)]


def t_cryptic_sorter():
    fixed = [[], ['a'], ['ccc', 'a', 'bb'], ['b', 'B', 'a', 'A'],
             ['banana', 'Apple', 'cherry', 'date', 'Fig', 'kiwi'],
             ['Abc', 'aBC', 'abc'], ['zz', 'Zz', 'aa', 'b']]
    rnd = [[rs('aAbBeE1z', 0, 4) for _ in range(R.randint(0, 9))] for _ in range(300)]
    return [(x,) for x in fixed + rnd]


def t_echo_validator():
    fixed = ['', 'a', 'Ana', 'A man a plan a canal Panama', 'abc', 'Race car',
             'No lemon, no melon', '12321', 'ab1ba', 'hello', 'Ab!Ba']
    return [(s,) for s in fixed] + [(rs('aAbB ,1', 0, 8),) for _ in range(300)]


def t_mirror_matrix():
    fixed = [[], [[]], [[1]], [[1, 2, 3], [4, 5, 6]], [[1, 2], [3, 4], [5, 6]]]
    rnd = [[[R.randint(-9, 9) for _ in range(R.randint(0, 5))]
            for _ in range(R.randint(0, 5))] for _ in range(200)]
    return [(m,) for m in fixed + rnd]


def t_hidenp():
    fixed = [('', ''), ('', 'abc'), ('abc', ''), ('fgex', 'tyfgdsxeq'),
             ('abc', 'aXbXc'), ('abc', 'acb'), ('aaa', 'aa'), ('A', 'a'),
             ('ace', 'abcde'), ('abc', 'abc')]
    return fixed + [(rs('abcA', 0, 4), rs('abcA', 0, 10)) for _ in range(400)]


def t_inter():
    fixed = [('', ''), ('abc', ''), ('', 'abc'), ('padinton', 'paqefwtdjetyiytjneytjoeyjnejeyj'),
             ('ddf6vewg64f', 'gtwthgdwthdwfteewhrtag6h4ffdhsd'), ('aaa', 'a'), ('Aa', 'a')]
    return fixed + [(rs('abcdA1 ', 0, 10), rs('abcdA1 ', 0, 10)) for _ in range(400)]


def t_number_base_converter():
    fixed = [('0', 10, 2), ('10', 10, 2), ('255', 10, 16), ('FF', 16, 10), ('Z', 36, 10),
             ('101', 2, 10), ('12', 2, 10), ('', 10, 2), ('10', 1, 10), ('10', 10, 37),
             ('10', 37, 10), ('1', 2, 36), ('G', 16, 10), ('007', 10, 10), ('35', 10, 36),
             ('ZZ', 36, 2), ('10', 0, 10), ('1A', 11, 10)]
    rnd = []
    for _ in range(300):
        fb, tb = R.randint(2, 36), R.randint(2, 36)
        rnd.append((rs('0123456789ABCDEFGHIJ', 1, 6), fb, tb))
    return fixed + rnd


def t_pattern_tracker():
    fixed = ['', '1', '12', '123456789', '90', '0123', 'a1b2', '1a2', '13', '21', '1212',
             '9012', '45 56']
    return [(s,) for s in fixed] + [(rs('0123456789a ', 0, 12),) for _ in range(400)]


def t_anagram():
    fixed = [('', ''), ('listen', 'silent'), ('Dormitory', 'dirty room'), ('abc', 'abd'),
             ('aab', 'abb'), ('A', 'a'), ('a b', 'ab'), ('abc', 'ab')]
    return fixed + [(rs('abcAB ', 0, 6), rs('abcAB ', 0, 6)) for _ in range(400)]


def t_shadow_merge():
    fixed = [([], []), ([1], []), ([], [2]), ([1, 3, 5], [2, 4, 6]), ([1, 1], [1]),
             ([-3, 0], [-5, 10])]
    rnd = [(sorted(R.randint(-9, 9) for _ in range(R.randint(0, 6))),
            sorted(R.randint(-9, 9) for _ in range(R.randint(0, 6)))) for _ in range(300)]
    return fixed + rnd


def t_string_permutation_checker():
    fixed = [('', ''), ('abc', 'cba'), ('abc', 'abC'), ('a b', 'ba '), ('a b', 'ab'),
             ('!!a', 'a!!'), ('aab', 'abb')]
    return fixed + [(rs('abA !', 0, 5), rs('abA !', 0, 5)) for _ in range(400)]


def t_string_sculptor():
    fixed = ['', 'a', 'hello', 'HELLO WORLD', 'a1b2c3', '123', 'aBc dEf!', '  x']
    return [(s,) for s in fixed] + [(rs(string.ascii_letters + ' 1!', 0, 12),) for _ in range(300)]


def t_twist_sequence():
    fixed = [([], 0), ([], 3), ([1], 5), ([1, 2, 3, 4, 5], 2), ([1, 2, 3], 0),
             ([1, 2, 3], 3), ([1, 2, 3], 4), ([1, 2, 3], 100)]
    rnd = [([R.randint(0, 9) for _ in range(R.randint(0, 7))], R.randint(0, 20))
           for _ in range(300)]
    return fixed + rnd


def t_whisper_cipher():
    fixed = [('', 3), ('abc', 1), ('xyz', 3), ('XYZ', 3), ('abc', -1), ('Hello, World!', 13),
             ('abc', 26), ('abc', -27), ('a1b2', 100)]
    return fixed + [(rs(string.ascii_letters + ' 1!', 0, 12), R.randint(-60, 60))
                    for _ in range(300)]


TESTS = {name[2:]: f for name, f in globals().items() if name.startswith('t_')}


# ---------------------------------------------------------------- checagens extras
def uses_forbidden(path, names):
    tree = ast.parse(open(path).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in names:
            return node.id + '()'
        if isinstance(node, ast.Attribute) and node.attr in names:
            return '.' + node.attr + '()'
    return None


FORBIDDEN = {'cryptic_sorter': {'sorted', 'sort'}}
NO_MUTATE = {'mirror_matrix', 'cryptic_sorter'}


def run_one(name, details):
    """Roda num processo separado. exit 0 = OK."""
    path = os.path.join(RENDU, name + '.py')
    if not os.path.isfile(path):
        print('arquivo rendu/%s.py nao existe' % name)
        return 2
    if name in FORBIDDEN:
        bad = uses_forbidden(path, FORBIDDEN[name])
        if bad:
            print('funcao proibida usada: ' + bad)
            return 1
    mod = types.ModuleType(name)
    mod.__file__ = path
    try:
        exec(compile(open(path).read(), path, 'exec'), mod.__dict__)
    except Exception as e:
        print('erro ao carregar o arquivo: %s: %s' % (type(e).__name__, e))
        return 1
    fn = getattr(mod, name, None)
    if not callable(fn):
        print('funcao %s nao encontrada no arquivo' % name)
        return 1
    ref = getattr(_refs(), name)
    for args in TESTS[name]():
        mine_args = copy.deepcopy(args)
        expected = ref(*copy.deepcopy(args))
        try:
            got = fn(*mine_args)
        except Exception as e:
            got = '<erro: %s: %s>' % (type(e).__name__, e)
        problem = got != expected
        if not problem and name in NO_MUTATE and mine_args != args:
            problem, got = True, '<a lista recebida foi modificada>'
        if problem:
            if details:
                print('entrada : %s(%s)' % (name, ', '.join(repr(a) for a in args)))
                print('esperado: %r' % (expected,))
                print('recebido: %r' % (got,))
            return 1
    return 0


def grade(name, details=False):
    try:
        p = subprocess.run([sys.executable, os.path.abspath(__file__), '--_run', name]
                           + (['-d'] if details else []),
                           capture_output=True, text=True, timeout=TIMEOUT)
        return p.returncode, p.stdout.strip()
    except subprocess.TimeoutExpired:
        return 1, 'timeout (loop infinito?)'


def level_of(name):
    for i, lv in enumerate(LEVELS):
        if name in lv:
            return i + 1


def show(name, code, msg, details):
    tag = 'OK' if code == 0 else ('--' if code == 2 else 'KO')
    print('  [%s] nivel %d  %s' % (tag, level_of(name), name))
    if msg and (details or code == 2):
        for line in msg.splitlines():
            print('        ' + line)


# ---------------------------------------------------------------- modo prova
def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return None


def save_state(st):
    json.dump(st, open(STATE, 'w'))


def prova():
    st = load_state()
    if st and st.get('level', 0) < len(LEVELS):
        if input('Continuar a prova salva (nivel %d)? [s/n] ' % (st['level'] + 1)).strip().lower() != 's':
            st = None
    else:
        st = None
    if st is None:
        st = {'level': 0, 'question': None, 'start': time.time(), 'tries': 0, 'log': []}
    while st['level'] < len(LEVELS):
        lv = LEVELS[st['level']]
        if st['question'] is None:
            st['question'] = R.choice(lv)
            save_state(st)
        q = st['question']
        mins = int((time.time() - st['start']) // 60)
        print('\n' + '=' * 70)
        print('NIVEL %d / %d   |   tempo: %d min   |   tentativas: %d'
              % (st['level'] + 1, len(LEVELS), mins, st['tries']))
        print('Escreva em: rendu/%s.py' % q)
        print('=' * 70)
        print(SUBJECTS[q])
        print('=' * 70)
        cmd = input('digite "grademe" para corrigir ou "sair" para parar: ').strip().lower()
        if cmd == 'sair':
            save_state(st)
            print('Prova salva. Rode --prova de novo para continuar.')
            return
        if cmd != 'grademe':
            continue
        st['tries'] += 1
        code, _ = grade(q)
        if code == 0:
            print('\n>>> OK! Proximo nivel.')
            st['log'].append([q, 'OK'])
            st['level'] += 1
        elif code == 2:
            print('\n>>> Arquivo rendu/%s.py nao encontrado. Nada foi corrigido.' % q)
            st['tries'] -= 1
            continue
        else:
            print('\n>>> KO. Nova questao sorteada no mesmo nivel.')
            st['log'].append([q, 'KO'])
        st['question'] = None
        save_state(st)
    mins = int((time.time() - st['start']) // 60)
    print('\nPROVA CONCLUIDA em %d min, %d tentativas.' % (mins, st['tries']))
    for q, r in st['log']:
        print('  %s  %s' % (r, q))
    save_state(st)


# ---------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    details = '-d' in args
    args = [a for a in args if a != '-d']
    if args[:1] == ['--_run']:
        sys.exit(run_one(args[1], details))
    if args[:1] == ['--prova']:
        try:
            prova()
        except (KeyboardInterrupt, EOFError):
            print('\nInterrompido. Progresso salvo.')
        return
    names = args or [n for lv in LEVELS for n in lv]
    for n in names:
        if n not in TESTS:
            print('questao desconhecida: %s' % n)
            return
    os.makedirs(RENDU, exist_ok=True)
    ok = 0
    print()
    for n in names:
        code, msg = grade(n, details)
        ok += code == 0
        show(n, code, msg, details)
    print('\n  %d / %d OK\n' % (ok, len(names)))


if __name__ == '__main__':
    main()
