#!/usr/bin/env python
# -*- coding: utf-8 -*-

PLUGINS = {}

# Load plugins that don't need any non-native package here
from plugins.quad_tree import QuadTreeIndex
# PLUGINS["Quad-Tree"] = QuadTreeIndex
from plugins.reverse_top_k.naive import ReverseTopKIndexNaive
# PLUGINS["Reverse Top-K Naive"] = ReverseTopKIndexNaive
from plugins.reverse_top_k.greedy import ReverseTopKIndexGreedy
# PLUGINS["Reverse Top-K Greedy"] = ReverseTopKIndexGreedy
from plugins.reverse_top_k.greedy0 import ReverseTopKIndexGreedy0
PLUGINS["Reverse Top-K Greedy"] = ReverseTopKIndexGreedy0


try:
    import rtree
except ImportError:
    print("[-] Missing LibSpatialIndex Rtree package.")
    print("[-] Rtree is disabled.")
else:
    from plugins.spatial_index_rtree import SpatialIndexRtree
    PLUGINS["Rtree"] = SpatialIndexRtree
