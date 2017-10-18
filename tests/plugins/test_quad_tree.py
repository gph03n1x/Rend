#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from plugins.quadTree import QuadTreeIndex
from random import randint
from tqdm import tqdm
import time

class FakeGUI:
    def heigth(self):
        return 250
    def width(self):
        return 250

class TestQuadTree(unittest.TestCase):


    def setUp(self):
        self.gui = FakeGUI
        self.index = QuadTreeIndex(self.gui)

    def test_quad_tree(self):
        # TODO: finish the unittest
        def test(n):

            points = list(set([
                (randint(0, 200), randint(0, 200)) for num in range(n)
                # (randint(0, 200), randint(0, 200), uuid.uuid4()) for num in range(n)
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


suite = unittest.TestLoader().loadTestsFromTestCase(TestQuadTree)
unittest.TextTestRunner(verbosity=2).run(suite)