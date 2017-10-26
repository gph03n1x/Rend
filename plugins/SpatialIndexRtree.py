from rtree import index
import math

class SpatialIndexRtree:
    GUI = {}
    def __init__(self, parent=None):
        self.idx = index.Index()
        self.ids = []
        self.count = 0

    def add_points(self, points):
        for point in points:
            self.ids.append(point)
            self.idx.insert(self.count, (point[0], point[1],point[0], point[1]))
            self.count += 1

    def intersection(self, x, y, r):
        # intersection uses box instead of circle
        #
        up_x, up_y, down_x, down_y = x - r, y - r, x + r, y + r
        # need to filter them out
        items = [self.ids[id] for id in list(self.idx.intersection((up_x, up_y, down_x, down_y)))]
        return list(filter(lambda item:self.point_in_circle(x, y, r, *item), items))

    def point_in_circle(self, center_x, center_y, radius, x, y, uuid=None):
        dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
        return dist <= radius

    def in_circle(self, x, y, r):
        # Future releases
        pass

    def nearest(self, x, y, k):
        return [self.ids[id] for id in list(self.idx.nearest((x, y, x, y), k))]