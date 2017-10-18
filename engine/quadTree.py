import math

class QuadTreeNode:
    THRESHOLD = 20
    def __init__(self, x, y, dx, dy, depth=1):
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
        self.nodes["NW"] = QuadTreeNode(self.x, self.y, self.center_x, self.center_y, self.depth + 1)
        self.nodes["NE"] = QuadTreeNode(self.center_x, self.y, self.dx, self.center_y, self.depth + 1)
        self.nodes["SW"] = QuadTreeNode(self.x, self.center_y, self.center_x, self.dy, self.depth + 1)
        self.nodes["SE"] = QuadTreeNode(self.center_x, self.center_y, self.dx, self.dy, self.depth + 1)
        #self.move_content_to_nodes()
        self.node_mode = True


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
    def __init__(self, boundaryX, boundaryY):
        self.root = QuadTreeNode(0, 0, boundaryX, boundaryY)
        self.count = 0

    def __str__(self):
        return self.root.__str__()

    def add(self, point):
        # TODO: create a non-recursion method


        node = self.root
        while True:
            if node.check_if_node_mode():
                node = node.get_direction_node(point)
            else:
                node.add(point)
                break

        q = [node]

        while q:
            node = q.pop()
            #print(node)
            #print("ok")
            if not node.is_stable():
                node.switch_to_node()
                node.move_content_to_nodes()
                q += list(node.nodes.values())


    def intersection(self, x, y, r):
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

    def nearest(self, x, y, k):
        pass

    def distance(self):
        pass


def test(n):
    from random import randint
    from tqdm import tqdm
    import uuid
    import time
    points = list(set([
        (randint(0, 200), randint(0, 200)) for num in range(n)
        #(randint(0, 200), randint(0, 200), uuid.uuid4()) for num in range(n)
    ]))
    a = QuadTreeIndex(200, 200)

    print(len(points))
    s = time.time()

    for point in tqdm(points):
        print(point)
        a.add(point)

    # print(a)
    cr = time.time() - s
    print("Adding took:", cr)

    s = time.time()
    r = a.intersection(110, 60, 30)
    intr = time.time() - s
    intr_c = a.count

    print("Intersecting took:", intr)
    print("Calculated for: ", a.count)
    print(sorted(r, key=lambda k: [k[1], k[0]]))
    a.count = 0
    s = time.time()
    results = []
    for point in points:
        if a.in_circle(110, 60, 30, point[0], point[1]):
            results.append(point)

    exudative = time.time() - s
    exu_c = a.count

    print("Checking them all took:", exudative)
    print("Calculated for: ", a.count)
    print(sorted(results, key=lambda k: [k[1], k[0]]))
    return (n, cr, intr, exudative, intr_c, exu_c)


if __name__ == "__main__":
    #ns = [100, 200, 1000, 2000, 10000, 20000, 100000, 200000]
    ns = [1000000]
    results = [test(n) for n in ns]
    print()
    print([r[0] for r in results])
    print([r[1] for r in results])
    print([r[2] for r in results])
    print([r[3] for r in results])
    print([r[4] for r in results])
    print([r[5] for r in results])



    #print(sorted(results, key=lambda k: [k[1], k[0]]))


