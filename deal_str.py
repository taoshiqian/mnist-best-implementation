

class TimeSegment(object):

    def __init__(self, segment, seconds):
        self.segments = [0 for i in range(24)]
        self.segments[segment] = seconds

    def __add__(self, other):
        ts = TimeSegment(0, 0)
        ts.segments = [x+y for x, y in zip(self.segments, other.segments)]
        return ts

    def __iadd__(self, other):
        self.segments = [x + y for x, y in zip(self.segments, other.segments)]
        return self

    def __str__(self):
        # return '|'.join([f'{seg}:{sec}' for seg, sec in self.segments])
       return '|'.join(f'{index}:{seconds}' for index, seconds in enumerate(self.segments) if seconds)


print(TimeSegment(13, 300) + TimeSegment(14, 300))


remain = 300
duration = 7200
hour = 13
result = duration - remain
h, s = divmod(result, 3600)
tss = []
tss.append(TimeSegment(hour, remain))
for i in range(h):
    tss.append(TimeSegment(hour +i + 1, 3600))
tss.append(TimeSegment(hour + h + 1, s))

import functools
print(functools.reduce(lambda x,y:x+y, tss))

# 13, 300
# 14, 3600
# 15, 3300

# RECORD = "ABCD|123|300|600|20180528135500"
#
# def _parse(record):
#     pass
#
# def _cal(start, duration):
#     return [(13, 300), (14,300)]
#
#
#
# def resolve(record):
#     # userId, start, duration = _parse(record)
#     userId, start, duration = ('ABCD',  '135500', '300')
#
#     #[()]
#     result = _cal(start, duration)
#     print( f'{userId}|'+ '|'.join([f'{x}:{y}' for x,y in result]))
#
#
# resolve(RECORD)



