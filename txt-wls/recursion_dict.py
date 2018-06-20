# -*- coding:utf-8 -*-


def fn(_dict, depth):
    if depth == 1:
        for k, v in _dict.items():
            yield k, v
    else:
        for k, v in _dict.items():
            yield from ( (k, *q) for q in fn(v, depth - 1) )


_dict = {
    # 'A': {
    #     'A1': [1, 2],
    #     'A2': [3, 4]
    # },
    # 'B': {
    #     'B1': [21, 22],
    #     'B2': [23, 24]
    # },
    'C': {
        'C1': {
            'c11':'c11'
        },
        'C2': {
            'c21':'c21',
            'c22':'c22'
        }
    }
}

for k, v, x, y in fn(_dict, 3):
    print(k, v, x, y)


_dict = {
    'A': {
        'A1': [1, 2],
        'A2': [3, 4]
    },
    'B': {
        'B1': [21, 22],
        'B2': [23, 24]
    }
}
for k, v, x in fn(_dict, 2):
    print(k, v, x)