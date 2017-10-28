#!/usr/bin/env python
# -*- coding: utf-8 -*-
from plugins.quadTree import QuadTreeIndex


PLUGINS = {}

# Load plugins that dont need any non-native package here
PLUGINS["Quad-Tree"] = QuadTreeIndex

try:
    import rtree
except ImportError:
    print("[-] Missing LibSpatialIndex Rtree package.")
    print("[-] Rtree is disabled.")
else:
    from plugins.SpatialIndexRtree import SpatialIndexRtree
    PLUGINS["[SptIdx] Rtree"] = SpatialIndexRtree
