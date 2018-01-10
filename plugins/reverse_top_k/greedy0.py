#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from collections import defaultdict
import ast
DIMENSIONS = 2


class ReverseTopKIndexGreedy0:
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
        self.posible_positions = defaultdict(int)
        q = [x,y]
        w = set()
        for i in range(k):
            dist = self.distances[i]
            points = self.distance_data[str(dist)]

            for point in points:
                w = self.get_advantages(point, q)
                for wi in w:
                    self.posible_positions[wi] += 1

        q_dist = math.sqrt(x**2+y**2)
        dist_ind = k
        dist = self.distances[dist_ind]
        points = self.distance_data[str(dist)]
        key_len = len(list(self.posible_positions.keys()))
        while dist < q_dist and key_len > 0:
            for point in points:
                for wi in self.posible_positions:

                    w = ast.literal_eval(wi)
                    q_score = sum(w[i]*q[i] for i in range(DIMENSIONS))
                    p_score = sum(w[i]*point[i] for i in range(DIMENSIONS))
                    if p_score < q_score:
                        self.posible_positions[wi] -= 1
            
                keys = list(self.posible_positions.keys())

                for key in keys:
                    if self.posible_positions[key] <= 0:
                        del self.posible_positions[key]

            dist_ind += 1
            dist = self.distances[dist_ind]
            points = self.distance_data[str(dist)]
            key_len = len(list(self.posible_positions.keys()))

        print(self.posible_positions)
        return [ast.literal_eval(key) for key in list(self.posible_positions.keys())]

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
"""
ind = ReverseTopKIndexGreedy0()
with open("data2.json", "r") as points_dat:
    import json
    json_data = json.load(points_dat)
    ind.load_json(json_data)
    print(ind.reverse_top_k(5, 500, 5))
    print(ind.reverse_top_k(5, 5, 5))
    print(ind.reverse_top_k(100, 200, 5))
    print(ind.reverse_top_k(1000, 20, 5))"""
