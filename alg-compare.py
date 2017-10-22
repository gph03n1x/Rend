from generate import generate_data
from plugins.SpatialIndexRtree import SpatialIndexRtree
from plugins.quadTree import QuadTreeIndex


import ast
import time
import matplotlib.pyplot as plt

class FakeGUI:
    @staticmethod
    def height():
        return 1000
    @staticmethod
    def width():
        return 1000


def load_points(dat_file):
    with open(dat_file, "r") as points_dat:
        return ast.literal_eval(points_dat.read())

ndata = [100, 500, 1000, 5000, 10000, 20000]

build_rtidx_time = []
build_qtidx_time = []
intersection_rtidx_time = []
intersection_qtidx_time = []
nearest_rtidx_time = []
nearest_qtidx_time = []

for n in ndata:
    print(n)
    points = generate_data(-500, 500, n)
    rtidx = SpatialIndexRtree()
    qtidx = QuadTreeIndex(FakeGUI)


    start_time = time.time()
    qtidx.add_points(points)
    build_qtidx_time.append(int((time.time() - start_time)*1000))

    start_time = time.time()
    rtidx.add_points(points)
    build_rtidx_time.append(int((time.time() - start_time)*1000))

    start_time = time.time()
    qtidx.intersection(10, 20, 30)
    intersection_qtidx_time.append(int((time.time() - start_time)*1000))

    start_time = time.time()
    rtidx.intersection(10, 20, 30)
    intersection_rtidx_time.append(int((time.time() - start_time)*1000))

    start_time = time.time()
    qtidx.nearest(10, 20, 30)
    nearest_qtidx_time.append(int((time.time() - start_time)*1000))

    start_time = time.time()
    rtidx.nearest(10, 20, 30)
    nearest_rtidx_time.append(int((time.time() - start_time)*1000))

print(intersection_qtidx_time)
print(intersection_rtidx_time)
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)
ax0.plot(ndata, build_qtidx_time, 'r--', label='Build time QuadTree')
ax0.plot(ndata, build_rtidx_time, 'k', label='Build time LibSpatialIndex Rtree ')
ax1.plot(ndata, intersection_qtidx_time, 'r--', label='Intersection time QuadTree')
ax1.plot(ndata, intersection_rtidx_time, 'k', label='Intersection time LibSpatialIndex Rtree')
ax2.plot(ndata, nearest_qtidx_time, 'r--', label='Nearest time QuadTree')
ax2.plot(ndata, nearest_rtidx_time, 'k', label='Nearest time LibSpatialIndex Rtree')

legend = ax0.legend(loc='upper center', shadow=True, fontsize='x-large')

legend.get_frame().set_facecolor('#00FFCC')

legend = ax1.legend(loc='upper center', shadow=True, fontsize='x-large')

legend.get_frame().set_facecolor('#00FFCC')

legend = ax2.legend(loc='upper center', shadow=True, fontsize='x-large')

legend.get_frame().set_facecolor('#00FFCC')

plt.show()

