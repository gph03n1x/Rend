#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from ast import literal_eval


class SpatialIndex:
    """
    Wrapper for the spatial indexes
    """

    def __init__(self, cardinal=None):
        """
        Initializes and creates a reference to the cardinal
        in order to update it whenever is needed.
        :param cardinal:
        """
        self.cardinal = cardinal
        self.index = None

    def set(self, plugin):
        """
        Initializes the index with the set plugin
        :param plugin:
        :return:
        """
        self.index = plugin()

    def load_points(self, dat_file):
        """
        Loads the points into the index if there is one.
        then if the cardinal is initialized it updates it.
        :param dat_file:
        :return:
        """
        if not self.index:
            return

        with open(dat_file, "r") as points_dat:
            points = literal_eval(points_dat.read())
            self.index.add_points(points)
            if self.cardinal:
                self.cardinal.points = points
                self.cardinal.update()

    def action(self, action_name, data):
        """
        Executes the action and passes the parameters while timing it.
        :param action_name:
        :param data:
        :return:
        """
        if not self.index:
            return {"metrics": {"time": 0}, "data": []}

        starting_time = time.time()
        detected = getattr(self.index, action_name)(**data)
        time_elapsed = time.time() - starting_time
        if self.cardinal:
            self.cardinal.update(detected)

        return {"metrics": {"time": time_elapsed}, "data": detected}
