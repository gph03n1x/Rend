#!/usr/bin/env python
# -*- coding: utf-8 -*-
from plugins.quadTree import QuadTreeIndex
from plugins.SpatialIndexRtree import SpatialIndexRtree

PLUGINS = {}

# Load plugins that dont need any non-native package here
PLUGINS["Quad-Tree"] = QuadTreeIndex

try:
    import rtree
except ImportError:
    print("[-] Missing LibSpatialIndex Rtree package.")
    print("[-] Rtree is disabled.")
else:
    PLUGINS["[SptIdx] Rtree"] = SpatialIndexRtree