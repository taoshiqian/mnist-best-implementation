RECORD = "ABCD|123|7200|7200|20180528135500"


class TimeSegment(object):
    def __init__(self, segment, second):
        self.segments = [0 for i in range(24)]
        self.segments[segment] = second

    def __add__(self, other):
        ts = TimeSegment(0,0)
        ts.segments = [x + y for x, y in zip(self.segments, other.segments)]
        return ts

    def __iadd__(self, other):
        self.segments = [x + y for x, y in zip(self.segments, other.segments)]
        return self

    def __str__(self):
        return '|'.join(f'{index}:{second}' for index, second in enumerate(self.segments) if second)


def parseTxt(txt):
    return "ABC", 1, 135500


def calc(duration, start_time):
    hour = start_time // 10000
    hasnot = start_time // 100 % 100 * 60 + start_time % 100
    end_time = hasnot + duration
    remain = min(3600 - hasnot, duration)
    h, s = divmod(end_time, 3600)
    tss = []
    tss.append(TimeSegment(hour, remain))
    for i in range(1,h):
        tss.append(TimeSegment(hour + i, 3600))
    tss.append(TimeSegment(hour + h, s))
    import functools
    result = functools.reduce(lambda x, y: x + y, tss)
    return result


def main():
    userId, duration, start_time = parseTxt(RECORD)
    result = calc(duration, start_time)
    print(userId,result)


if __name__ == '__main__':
    main()
