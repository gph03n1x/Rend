#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from plugins.quadTree import QuadTreeIndex
from random import randint
import time
import queue


class TestQuadTree(unittest.TestCase):

    def setUp(self):
        QuadTreeIndex.GUI = {
            'WIDTH': 1000,
            'HEIGHT': 1000
        }
        self.index = QuadTreeIndex()
        #"""
        self.points = list(set([

            (randint(-500, 500), randint(-500, 500)) for num in range(100000)
        ]))
        #"""
        """
        with open("errorpoints.dat", "r") as points_dat:
            self.points = literal_eval(points_dat.read())
        """

        s = time.time()
        self.index.add_points(self.points)
        cr = time.time() - s
        print("Adding took: {0}ms".format(int(round(cr * 1000))))

    def test_intersection(self):
        s = time.time()
        r = self.index.intersection(110, 60, 30)
        intr = time.time() - s

        print("Using quadtree: intersection took {0}ms, visited {1} nodes".format(
            int(intr * 1000), self.index.count)
        )

        r = sorted(r, key=lambda k: [k[1], k[0]])

        self.index.count = 0
        s = time.time()
        results = [point for point in self.points if self.index.in_circle(110, 60, 30, point[0], point[1])]
        results = sorted(results, key=lambda k: [k[1], k[0]])
        exudative = time.time() - s

        print("Using exudative search: intersection took {0}ms, visited {1} nodes".format(
            str(int(exudative * 1000)), str(self.index.count))
        )

        self.assertEqual(r, results)

    def test_nearest(self):
        # we are using the sorted closer distances and not the points themselves because
        # because there might be two points with same distance and each algorithm can pick
        # a different one than the other, which is ok.
        s = time.time()
        r = self.index.nearest(110, 60, 30, debug=True)
        intr = time.time() - s

        print("Using quadtree: nearest took {0}ms, visited {1} nodes".format(
            int(intr * 1000), self.index.count)
        )
        r.sort()

        p = queue.PriorityQueue()
        self.index.count = 0
        s = time.time()

        for point in self.points:
            p.put((-self.index.point_distance(110, 60, *point), point))

        results = [p.get()[0] for i in range(30)]

        exudative = time.time() - s

        print("Using exudative search: nearest took {0}ms, visited {1} nodes".format(
            str(int(exudative * 1000)), str(self.index.count))
        )

        self.assertEqual(r, results)

        """
        if self.assertRaises(TypeError):
            with open("errorpoints.dat", "w") as points_dat:
                points_dat.write(str(self.points))
        """


suite = unittest.TestLoader().loadTestsFromTestCase(TestQuadTree)
unittest.TextTestRunner(verbosity=2).run(suite)