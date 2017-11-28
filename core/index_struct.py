
class SpatialIndex:

    def __init__(self, plugin):
        self.index = plugin()
        

    def add_points(self, points):
        self.index.add_points(self.points)

    def status(self):
        pass

    def action(self, action_name):
        # getattr(self.index, action_name)()
        pass
    
    def get_actions(self):
        pass
