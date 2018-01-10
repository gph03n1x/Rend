#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from collections import defaultdict
import ast
DIMENSIONS = 2


class ReverseTopKIndexGreedy:
    PARAMETERS = {
        "visual": False,
        "data_extensions": ["*.json"],
        "elements": [],
        "data": {}

    }
    ACTIONS = {
        "Reverse Top-K": {
            "action": "reverse_top_k",
            "elements": {
                "x,y": "PointEditFloat",
                "k": "LabelEditInt"
            },
            "data": {}
        }
    }

    def __init__(self):
        self.weights = []
        self.points = []
        self.distances = []
        self.distance_data = defaultdict(list)

    def load_json(self, json_data):
        self.weights = json_data["weights"]
        self.points = json_data["points"]
        self.weights.sort()
        self.str_weights = [str(weight) for weight in self.weights]

        for point in self.points:
            distance = math.sqrt(point[0] ** 2 + point[1] ** 2)
            self.distance_data[str(distance)].append(point)
            self.distances.append(distance)
        self.distances.sort()

    def get_points(self):
        return self.points

    def add_points(self, points):
        pass

    def reverse_top_k(self, x, y, k):
        q = [x,y]
        w = set()
        for i in range(k):
            dist = self.distances[i]
            points = self.distance_data[str(dist)]
            print(w)
            for point in points:
                if w:
                    w = w | self.get_advantages(point, q)
                else:
                    w = self.get_advantages(point, q)

        print(w)
        w = [ast.literal_eval(wi) for wi in list(w)]
        print(w)
        return w

    def get_advantages(self, point, q):
        if q[0] < point[0] and q[1] < point[0]:
            print("All")
            return set(self.str_weights)
        elif q[0] <= point[0] and q[1] <= point[0]:
            print("none")
            return set([])
        else:
            d = 0.5 + 0.5 * (point[0] - q[0]) / q[0]
            print("d", d)
            if d < 0 or d > 1:
                print("under or overweight")
                return set([])
            ind = self.slow_weight_search(d)

            if q[0] > point[0]:
                print("until", ind)
                return set(self.str_weights[:ind])
            else:
                print("after", ind)
                return set(self.str_weights[ind:])

    def slow_weight_search(self, d):
        for p, weight in enumerate(self.weights):
            if d > weight[0]:
                continue
            if d < weight[0]:
                return p
        return -1
