#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict

DIMENSIONS = 2


class ReverseTopKIndexNaive:
    PARAMETERS = {
        "visual": True,
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
        self.counter = defaultdict(int)

    def load_json(self, json_data):
        self.weights = json_data["weights"]
        self.points = json_data["points"]

    def get_points(self):
        return self.points

    def add_points(self, points):
        pass

    def reverse_top_k(self, x, y, k):
        self.counter = defaultdict(int)
        self.Q = [x, y]
        l = len(self.points)
        for weight in self.weights:
            q_score = sum(weight[i]*self.Q[i] for i in range(DIMENSIONS))
            for point in self.points:
                p_score = sum(weight[i]*point[i] for i in range(DIMENSIONS))
                if q_score < p_score:
                    self.counter[str(weight)] += 1
            self.counter[str(weight)] = l - self.counter[str(weight)]
        print(self.counter)
        return [weight for weight in self.weights if self.counter[str(weight)] < k]
