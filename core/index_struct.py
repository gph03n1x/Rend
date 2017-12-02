#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from ast import literal_eval


class SpatialIndex:

    def __init__(self, cardinal=None):
        self.cardinal = cardinal
        self.index = None

    def set(self, plugin):
        self.index = plugin()

    def load_points(self, dat_file):
        if not self.index:
            return

        with open(dat_file, "r") as points_dat:
            points = literal_eval(points_dat.read())
            self.index.add_points(points)
            if self.cardinal:
                self.cardinal.points = points
                self.cardinal.update()

    def action(self, action_name, data):
        if not self.index:
            return 0, []

        t = time.time()
        detected = getattr(self.index, action_name)(**data)
        time_elapsed = time.time() - t
        if self.cardinal:
            self.cardinal.update(detected)

        return {"metrics": {"time": time_elapsed}, "data": detected}
