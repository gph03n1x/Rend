#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import queue
# TODO: heap attempts to compare Nodes
class QuadTreeNode:
    THRESHOLD = 20
    def __init__(self, x, y, dx, dy, depth=1, id="0"):
        self.id = id
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = dx-x
        self.height = dy-y
        self.center_x = (x+dx)/2
        self.center_y = (y+dy)/2

        self.nodes = {
            "NW": None,
            "NE": None,
            "SW": None,
            "SE": None,
        }

        self.depth = depth
        self.shadow = True
        self.node_mode = False

        self.content = []
        self.count = 0
        self.connected = []

    def rect(self):
        return (self.x, self.y, self.width, self.height)

    def switch_to_node(self):
        # TODO: oh boi
        self.nodes["NW"] = QuadTreeNode(self.x, self.y, self.center_x, self.center_y, self.depth + 1, self.id+"1")
        self.nodes["NE"] = QuadTreeNode(self.center_x, self.y, self.dx, self.center_y, self.depth + 1, self.id+"2")
        self.nodes["SW"] = QuadTreeNode(self.x, self.center_y, self.center_x, self.dy, self.depth + 1, self.id+"3")
        self.nodes["SE"] = QuadTreeNode(self.center_x, self.center_y, self.dx, self.dy, self.depth + 1, self.id+"4")
        #self.move_content_to_nodes()
        self.node_mode = True

    def __lt__(self, other):
        return self.id < other.id

    def __str__(self):
        result = "({0},{1}) : ({2},{3})\n".format(self.x, self.y, self.dx, self.dy)
        if self.node_mode:
            result += self.depth*"\t" + "NW: {0}".format(self.nodes["NW"])
            result += self.depth*"\t" + "NE: {0}".format(self.nodes["NE"])
            result += self.depth*"\t" + "SW: {0}".format(self.nodes["SW"])
            result += self.depth*"\t" + "SE: {0}".format(self.nodes["SE"])
        else:
            result += self.depth*"\t" + "-> " + str(self.content) + "\n"
        return result

    def add(self, point):
        if self.shadow == True:
            self.shadow = False

        self.content.append(point)
        self.count +=1

    def is_stable(self):
        if self.count >= QuadTreeNode.THRESHOLD:
            return False
        return True

    def check_if_node_mode(self):
        return self.node_mode


    def move_point_nodes(self, point):
        pos = ""
        # looks ugly
        if point[1] > self.center_y:
            pos += "S"
        else:
            pos += "N"

        if point[0] > self.center_x:
            pos += "E"
        else:
            pos += "W"

        self.nodes[pos].add(point)

    def get_direction_node(self, point):
        pos = ""
        # looks ugly
        if point[1] > self.center_y:
            pos += "S"
        else:
            pos += "N"

        if point[0] > self.center_x:
            pos += "E"
        else:
            pos += "W"

        return self.nodes[pos]


    def move_content_to_nodes(self):
        for point in self.content:
            self.move_point_nodes(point)
        self.content = []


class QuadTreeIndex:
    GUI = {
        'WIDTH': 100,
        'HEIGHT': 100
    }

    def __init__(self, parent=None):
        self.X = self.GUI['WIDTH']
        self.Y = self.GUI['HEIGHT']
        print(self.X, self.Y)
        self.root = QuadTreeNode(-self.X, -self.Y, self.X, self.Y)
        self.count = 0

    def __str__(self):
        return self.root.__str__()

    def add_points(self, points):
        for point in points:
            if point[0] >= -self.X and point[0] <= self.X and point[1] >= -self.Y and point[1] <= self.Y:
                self.add(point)
            else:
                print("[-] Discarded point", str(point))
    def add(self, point):
        node = self.root
        # Find the node where the point should get into
        while True:
            if node.check_if_node_mode():
                node = node.get_direction_node(point)
            else:
                node.add(point)
                break

        # Split the node if needed and split whichever node needs splitting
        q = [node]

        while q:
            node = q.pop()
            if not node.is_stable():
                node.switch_to_node()
                node.move_content_to_nodes()
                q += list(node.nodes.values())


    def intersection(self, x, y, r):
        self.count = 0
        queue = [self.root]
        results = []

        while queue:
            atom_rect = queue.pop()
            if not atom_rect.node_mode:
                # check if they part
                for point in atom_rect.content:
                    if self.in_circle(x, y, r, point[0], point[1]):
                        results.append(point)
            else:
                for node in atom_rect.nodes:
                    if atom_rect.nodes[node].shadow:
                        continue
                    if self.are_intersecting(x, y, r, *atom_rect.nodes[node].rect()):
                        queue.append(atom_rect.nodes[node])

        return results

    def in_circle(self, center_x, center_y, radius, x, y):
        self.count += 1
        dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
        return dist <= radius

    def are_intersecting(self, cx, cy, cr, rx, ry, rw, rh):
        self.count += 1
        distX = abs(cx - rx - rw / 2)
        distY = abs(cy - ry - rh / 2)

        if (distX > (rw / 2 + cr)):
            return False
        if (distY > (rh / 2 + cr)) :
            return False

        if (distX <= (rw / 2)) :
            return True
        if (distY <= (rh / 2)) :
            return True

        dx = distX - rw / 2
        dy = distY - rh / 2

        return (dx ** 2 + dy ** 2 <= (cr ** 2))

    def nearest(self, x, y, k, debug=False):
        self.count = 0
        boxes = queue.PriorityQueue()
        points = []
        boxes.put((self.box_distance(x, y, *self.root.rect()), self.root))
        while not boxes.empty() and len(points) < k:
            current_box = boxes.get()
            
            if not isinstance(current_box[1], QuadTreeNode):
                points.append(current_box)
                continue

            if current_box[1].shadow:
                continue

            if current_box[1].node_mode:
                #print(self.box_distance(x, y, *current_box[1].nodes["SE"].rect()))
                boxes.put((self.box_distance(x, y, *current_box[1].nodes["SE"].rect()), current_box[1].nodes["SE"]))
                boxes.put((self.box_distance(x, y, *current_box[1].nodes["SW"].rect()), current_box[1].nodes["SW"]))
                boxes.put((self.box_distance(x, y, *current_box[1].nodes["NE"].rect()), current_box[1].nodes["NE"]))
                boxes.put((self.box_distance(x, y, *current_box[1].nodes["NW"].rect()), current_box[1].nodes["NW"]))
            else:
                for point in current_box[1].content:
                    boxes.put((self.point_distance(x, y, *point), point))

        if debug:
            return [point[0] for point in points]
        return [point[1] for point in points]

    def point_distance(self, x, y, px, py, uuid=None):
        # should be negative to be like a reverse priority queue
        self.count += 1
        return math.hypot(x - px, y - py)


    def box_distance(self, x, y, rx, ry, rw, rh):
        self.count +=1
        # TODO: ugh
        if x < rx:
            closer_X = rx
        elif x > rx+rw:
            closer_X = rx+rw
        else:
            closer_X = x

        if y < ry:
            closer_Y = ry
        elif y > ry+rh:
            closer_Y = ry+rh
        else:
            closer_Y = y

        return self.point_distance(x, y, closer_X, closer_Y)
