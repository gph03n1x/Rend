import time
from ast import literal_eval

class SpatialIndex:

    def __init__(self, cardinal):
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
            self.cardinal.points = points
            self.cardinal.update()

    def action(self, action_name, data):
        if not self.index:
            return 0, []

        t = time.time()
        detected = getattr(self.index, action_name)(**data)
        time_elapsed = time.time() - t
        self.cardinal.update(detected)

        return time_elapsed, detected
