# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 10:40:03 2019

@author: Imre Antalfy
"""

import numpy as np

P3_Input = {(1,2) : ('AAACATCCAAACACCA--ACCCCAG-',
'ACCAAACCTGTCCCCATCTAACACCA'),
(1,3) : ('AAACATCCAAAC-ACCAACCCCAG-',
'AAT-ACCCAACTCGACCTACACCAA'),
(2,3) : ('ACCAAACCTGTCCCCATCTAACACCA',
'A-ATACCCAACTCGACCTA-CACCAA')}



    
########################
### Input Check functions

def CheckSeq(Seq):
    """ Checking seq
    only allowed chars in Seq are A,C,G,T. if Seq differs, raise an error
    """
    OkNucleo = ("A", "C", "G", "T", "-")
    for i in Seq:
        if i not in OkNucleo:
            raise Exception(Seq,"malformed input") 

def ComputeExpKey(seq_dict):
    """ compute the expected keys based on the size of the input dictionary
        and return it as a list
    """
    exp_key = []
    m = 1
    while m <= len(seq_dict):   
        n = m + 1
        while n <= len(seq_dict):
            exp_key.append((m,n))
            n += 1
        m += 1    
    return(exp_key)

def CheckInput(dictionary):
    """ takes the input dictionary and checks if pairs are in the awaited
        order and if sequences are not violated
    """
    
    exp_keys = ComputeExpKey(dictionary)
    if  exp_keys != list(dictionary.keys()):
        raise Exception("malformed input")
        
    for sequence in dictionary.values():
         CheckSeq(sequence[0])
         CheckSeq(sequence[1])

########################
### Functions
        
  
# Calculation functions
def DelMissLinks(seq_A, seq_B):
    """ Deletes all missing entries of the sequences of a pair for comparison
    """
    seq_A_new = ""
    seq_B_new = ""
    for x, y in zip(seq_A, seq_B):
        if not x == "-" or y == "-":
            seq_A_new += "".join(x)
            seq_B_new += "".join(y)  
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
    """ Calculate the distances for all pairs in the fiven data
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

# storage function
def DistMatrix(distance_list):
    """filling the distance matrix with the genomic distances
        takes the computed distance list and an input
        reuturns the filled distance matrix
    """

    m_size = len(distance_list)
    matrix = np.zeros((m_size,m_size))
    
    m = 0 #index a for matrix
    x = 0 #index in distance list
    
    while m <= m_size-1:   
        n = m + 1
        while n <= m_size-1:
            matrix[m,n] = distance_list[x]
            matrix[n,m] = distance_list[x]    
            x += 1
            n += 1
        m += 1
    return(matrix)

########################
### Main function
        
def ComputeDistMatrix(sequence_dict):
    """ check input, compute all distances, put all distances into matrix
        takes a dictionary with genetic pairs and their sequences
        returns the distance matrix for all couples
    """
    CheckInput(sequence_dict)
    # calculate distances
    evol_distances = AllDist(sequence_dict)
    # open and fill distance matrix
    result = DistMatrix(evol_distances)
    return( result.tolist() )

########################
### Main function Call
    
print( ComputeDistMatrix(P3_Input) )
