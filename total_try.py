# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:06:13 2019

@author: Imre Antalfy
"""

import P1
import P2
import P3
import P4



Parsed = P1.ParseSeqFile("sequence.txt")

Aligned = P2.AlignByDP(Parsed)

Dist_Mat = P3.ComputeDistMatrix(Aligned)

labels = ['Mouse','Bovine','Gibbon','Orangutan','Gorilla','Chimp','Human']
   
P4.Cluster(Dist_Mat,labels)
