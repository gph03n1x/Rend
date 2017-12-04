#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ReverseTopK:
    PARAMETERS = {
        "visual": True,
        "elements": [],
        "data": {}

    }
    ACTIONS = {
        "Reverse Top-K": {
            "action": "reverse_top_k",
            "elements": {
                "x,y": "PointEdit",
                "k": "LabelEditFloat"
            },
            "data": {}
        }
    }

    def add_points(self, points):
        pass

    def reverse_top_k(self, x, y, k):
        pass
