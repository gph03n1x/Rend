import bisect
# An index based on the x-keystone and the y keystone.


class Keystone:
    def __init__(self):
        self.point_index = {}
        self.ordered_index = []
        self.count = 0

    def add_index(self, key, value):
        self.point_index[key] = value
        bisect.insort(self.ordered_index, key)
        self.count += 1

    def get_bounds(self, before, after, lower, upper):
        print(before, after, lower, upper)
        if before - lower < 0:
            lower = before  # k_index - below equals 0
        if after + upper > self.count - 1:
            upper = self.count - after  # k_index + above equals self.count - 1

        return before - lower, after + upper

    def get_in_range(self, lower, upper):
        # TODO: bounds should be based on the radious
        keys = [
            self.ordered_index[key] for key in range(lower, upper)
        ]
        print(keys)
        return [self.point_index[key] for key in keys]

    def get_closer_bounds(self, center):
        """
        https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value/
        Assumes myList is sorted. Returns closest value to myNumber.

        If two numbers are equally close, return the smallest number.
        """
        pos = bisect.bisect_left(self.ordered_index, center)
        if pos == 0:
            return 0, 0
        if pos == self.count:
            return -1, -1
        before = pos - 1
        after = pos
        return before, after

    def get_box_bounds(self, center, distance):
        upper = self.get_closer_bounds(center + distance)[0]
        lower = self.get_closer_bounds(center - distance)[1]
        return lower, upper


class Point:
    def __init__(self, x, y, data):
        # TODO: prediction moving data
        self.x = x
        self.y = y
        self.data = data

