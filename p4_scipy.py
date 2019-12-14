# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 18:34:39 2019

@author: Imre Antalfy
"""

from scipy.cluster.hierarchy import weighted, fcluster
from scipy.cluster.hierarchy import dendrogram
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

import sys
sys.path.append("C:\Users\Imre Antalfy\Documents\GitHub\HardBoiledEggs")
import p3.py

test = [[0.0, 1.2518678603517923, 1.0506698704057822], [1.2518678603517923, 0.0, 2.747671234597231], [1.0506698704057822, 2.747671234597231, 0.0]]

test

y = pdist(test)

Z = weighted(y)


plt.figure()
dn = hierarchy.dendrogram(Z)
plt.show()