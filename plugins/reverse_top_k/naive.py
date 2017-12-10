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
        self.Q = []
        self.score = defaultdict(dict)
        self.counter = defaultdict(dict)

    def load_json(self, json_data):
        self.weights = json_data["weights"]
        self.Q = json_data["points"]

        for weight in self.weights:
            for q in self.Q:
                self.score[str(weight)][str(q)] = sum(weight[i]*q[i] for i in range(DIMENSIONS))

    def get_points(self):
        return self.Q

    def add_points(self, points):
        pass

    def reverse_top_k(self, x, y, k):
        print(self.score)
        return []
