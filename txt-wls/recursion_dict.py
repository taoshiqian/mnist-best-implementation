# -*- coding:utf-8 -*-
# 递归实现多重for循环的函数
def fn(_dict, depth):
    if depth == 1:
        for k, v in _dict.items():
            yield k, v
    else:
        for k, v in _dict.items():
            yield from ((k, *q) for q in fn(v, depth - 1))

# 双重dict
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
# 一句话遍历双重dict
for k, v, x in fn(_dict, 2):
    print(k, v, x)
print()
print()


# 三重dict
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
            'c11': 'c11'
        },
        'C2': {
            'c21': 'c21',
            'c22': 'c22'
        }
    },
    'D': {
        'D1': {
            'd11': 123
        }
    }
}
# 一句话遍历三重dict
for k, v, x, y in fn(_dict, 3):
    print(k, v, x, y)
print()
print()


# 土方法的三重循环,太丑了
for k1, v1 in _dict.items():
    for k2, v2 in v1.items():
        for k3, v3 in v2.items():
            print(k1, k2, k3, v3)
