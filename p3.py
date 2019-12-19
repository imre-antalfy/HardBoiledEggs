# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 10:40:03 2019

@author: Imre Antalfy
"""

import numpy as np
from collections import defaultdict
    
############################################################
### 00 - Input Check functions

def CheckInput(Input):
    """ Check if input is dict(tuple(int,int) -> tuple(str,str))
    """
    if type(Input) != defaultdict:
        raise Exception(Input, "malformed input")
        
    for key,value in Input.items():
        if type(key) != tuple or type(value) != tuple:
            raise Exception(key, "malformed input")
        
        for item in key:
            if type(item) != int:
                raise Exception(key, "malformed input")
                
        for item in value:
            if type(item) != str:
                raise Exception(key, "malformed input")

############################################################
### 01 - distance calculation functions
                
def DelMissLinks(seq_A, seq_B):
    """ Deletes all missing entries of the sequences of a pair for comparison
    returns both cleaned sequences
    """
    seq_A_new = ""
    seq_B_new = ""
    for charA, charB in zip(seq_A, seq_B):
        if (charA != '-') and (charB != '-'):
            seq_A_new += "".join(charA)
            seq_B_new += "".join(charB)
    return(seq_A_new,seq_B_new)
    
def CountTotDiff(seq_A, seq_B):
    """ Takes both sequences of a pair as an input 
    returns the genomic difference
    """
    diff = 0
    for x, y in zip(seq_A, seq_B):
        if x != y:
            diff += 1
    p = diff / len(seq_A)
    return(p)

def CalcEvolDist(p):
    """ Evolutionary distance in between a gene pair
    based on differences of the sequences of the pair, 
    compute distance. If differences are 0 or >= 3/4, set dist =30
    """
    if p >= 3/4 or p == 0:
        result = 30
    else: 
        result = -(3/4) * np.log(1 - 4/3*p)
    return(result)

def AllDist(sequence_dict):
    """ Calculate the distances for all pairs in the given data
    key per key
    returns a list of calculated distances
    """
    dist = []
    for pair in sequence_dict.values():
        seq_A = pair[0]
        seq_B = pair[1]
        seq_A, seq_B = DelMissLinks(seq_A, seq_B)     
        p = CountTotDiff(seq_A, seq_B)
        dist.append(CalcEvolDist(p))
    return(dist)

############################################################
### 02 - Matrix function
    
    #the error is here
def DistMatrix(distance_list):
    """filling the distance matrix with the genomic distances
    takes the computed distance list and an input
    returns the filled distance matrix
    """

    m_size = int(len(distance_list)/3) # care for error, test again!!!
    matrix = np.zeros((m_size,m_size))
    
    m = 0 #index a for matrix 
    x = 0 #index in distance list
    while m <= m_size-1:   
        n = m + 1 #index b for matrix 
        while n <= m_size-1:
            matrix[m,n] = distance_list[x]
            matrix[n,m] = distance_list[x]    
            x += 1
            n += 1
        m += 1
    return(matrix)

############################################################
### 10 - Main function
        
def ComputeDistMatrix(sequence_dict):
    """ check input, compute all distances, put all distances into matrix
    takes a dictionary with genetic pairs and their sequences
    returns the distance matrix for all couples
        as list(list(float))
    """
    CheckInput(sequence_dict)
    evol_distances = AllDist(sequence_dict)    
    result = DistMatrix(evol_distances)
    return(result.tolist())
