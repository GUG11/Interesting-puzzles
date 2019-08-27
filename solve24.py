from typing import List, Dict
from copy import deepcopy
from itertools import chain
import pprint
import re

pp = pprint.PrettyPrinter()

OPS = ['+', '-', '*', '/']

digit_pat = re.compile('\d+')


def _select(cards: List[int], n: int, s: int, candidate: List[int], result: List[List[int]]) -> None:
    if n == 0:
        result.append(deepcopy(candidate))
    else:
        for i in range(s, len(cards) - n + 1):
            if s < i and cards[i] == cards[i-1]:
                continue
            candidate.append(cards[i])
            _select(cards, n - 1, i + 1, candidate, result)
            candidate.pop()

def select(cards: List[int], n: int) -> List[List[int]]:
    result = []
    _select(cards, n, 0, [], result)
    return result

def enumerate_subseqs(cards: List[int]) -> List[List[int]]:
    size = len(cards)
    subseqs = map(lambda i: select(cards, i), range(1, size))
    return list(chain(*subseqs))


def compute(cards: List[int]) -> Dict[int, List[str]]:
    if len(cards) == 1:
        return {cards[0]: [str(cards[0])]}
    left_choices = enumerate_subseqs(cards)
    res = {}
    for left in left_choices:
        right = deepcopy(cards)
        for elem in left:
            right.remove(elem)
        left_res_kvs = compute(left)
        right_res_kvs = compute(right)
        for op in OPS:
            for lk, lv in left_res_kvs.items():
                for rk, rv in right_res_kvs.items():
                    # TODO: commutative operators
                    if op == '+':
                        res_k = lk + rk
                    if op == '-':
                        res_k = lk - rk
                        if res_k < 0:
                            continue
                    if op == '*':
                        res_k = lk * rk
                    if op == '/':
                        if rk == 0 or lk % rk != 0:
                            continue
                        res_k = lk // rk
                    if res_k not in res:
                        res[res_k] = []
                    for lexp in lv:
                        for rexp in rv:
                            # TODO: refine the expression generation
                            if digit_pat.match(lexp) is not None or op in ('+', '-'):
                                exp = '{}'
                            else:
                                exp = '({})'
                            exp = exp + ' {} '
                            if digit_pat.match(rexp) is not None:
                                exp = exp + '{}'
                            else:
                                exp = exp + '({})'
                            res[res_k].append(exp.format(lexp, op, rexp))
    return res

if __name__ == '__main__':
    # cards = [3, 6, 6, 11]
    cards = [3, 5, 7, 13]
    # cards = [2, 3, 5, 12]
    res = compute(cards)
    pp.pprint(res)
    pp.pprint('correct result:')
    pp.pprint(res[24])
