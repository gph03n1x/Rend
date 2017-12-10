#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rtree import index
import math


class SpatialIndexRtree:
    PARAMETERS = {
        "visual": True,
        "data_extensions": ["*.dat"],
        "elements": [],
        "data": {}
    }

    ACTIONS = {
        "Search in circle": {
            "action": "inside_circle",
            "elements": {
                "x,y": "PointEditInt",
                "radius": "LabelEditInt"
            },
            "data": {}
        },
        "Search in box": {
            "action": "inside_box",
            "elements": {
                "left_x,up_y": "PointEdit",
                "right_x,down_y": "PointEdit",
            },
            "data": {}
        },
        "Nearest K": {
            "action": "nearest",
            "elements": {
                "x,y": "PointEditFloat",
                "k": "LabelEditInt"
            },
            "data": {}
        }

    }

    def __init__(self):
        self.idx = index.Index()
        self.item_ids = []
        self.count = 0

    def add_points(self, points):
        for point in points:
            self.item_ids.append(point)
            self.idx.insert(self.count, (point[0], point[1], point[0], point[1]))
            self.count += 1

    def inside_box(self, left_x, up_y, right_x, down_y):
        return [self.item_ids[item_id] for item_id in list(self.idx.intersection((left_x, up_y, right_x, down_y)))]

    def point_in_circle(self, center_x, center_y, radius, x, y, uuid=None):
        dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
        return dist <= radius

    def inside_circle(self, x, y, radius):
        left_x, up_y, right_x, down_y = x - radius, y - radius, x + radius, y + radius
        items = self.inside_box(left_x, up_y, right_x, down_y)
        return list(filter(lambda item: self.point_in_circle(x, y, radius, *item), items))

    def nearest(self, x, y, k):
        return [self.item_ids[item_id] for item_id in list(self.idx.nearest((x, y, x, y), k))]
