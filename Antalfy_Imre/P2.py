# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:43:07 2019

@author: Imre Antalfy
"""

import numpy as np
import pandas as pd
from collections import defaultdict

############################################################
### 00 - input check

def CheckInput(Input):
    """ Check if input is list(tuple(string,string)))
    """
    if type(Input) != list:
        raise Exception(Input, "malformed input")

    for row in Input:
        if type(row) != tuple:
            raise Exception(row, "malformed input")
            
        for value in row:
            if type(value) != str:
                raise Exception(value, "malformed input")
                
############################################################
### 01 - matrix setup functions
                
def CreateDynamicMatrix(n_cols, n_rows, penalty):
    """  Dynamic programming matrix
    integer matrix, keeping track of the evolutionary score
    penalty scores in first row & colum calculated, otherwise empty
    return matrix
    """
    Matrix = np.zeros(shape=(n_rows,n_cols), dtype=np.int)
 
    # starting values
    for i in range(1, n_rows):
        Matrix[i][0] = Matrix[i-1][0] - penalty
    
    for j in range(1, n_cols):
        Matrix[0][j] = Matrix[0][j-1] - penalty
    
    return(Matrix)

def CreateTracebackMatrix(n_cols, n_rows):
    """ Traceback matrix
    String matrix, keeping track of the decision taken by the calculation
    the first row and column are prefilled, as the decision is always the same
    return matrix
    """
    Matrix = np.full(shape=(n_rows, n_cols), fill_value=" ", dtype=np.str)
    
    Matrix[0][0] = "•"
    for i in range(1, n_rows):
        Matrix[i][0] = "↑"
    
    for j in range(1, n_cols):
        Matrix[0][j] = "←"
    
    return(Matrix)
    
############################################################
### 02 - calculation/update functions
    
def WriteTraceback(traceback_matrix, current_cell, result_list, 
                   index_row, index_col):
    """ Filling Traceback matrix
    from result list, first list entry is instertion, 2nd gaprow, 3d gapcol
    "↖" = case insertion
    "↑" = case gap row
    "←" = case gap columm 
    """
    if current_cell == result_list[0]: # case insertion
        traceback_matrix[index_row][index_col] = "↖" 
        
    elif current_cell == result_list[1]: # case gap row
        traceback_matrix[index_row][index_col] =  "↑"
        
    else: #case gap column
        traceback_matrix[index_row][index_col] =  "←"


def FillMatrices(dynamic_matrix, traceback_matrix, substitution_matrix, 
                 n_rows, n_cols, seq1, seq2, penalty):
    """ Calculation of dynamic score and traceback function call
    evolutionary score calculation of M[i][j]
    three possibilities, take maximum the three calculations,
    insertion:
        M[i-1][j-1] + S[ci][cj] (c = char of current sequence)
    gap in row:
        M[i-1][j] - penalty
    gap in col:
        M[1][j-1] - penalty
        
    traceback matrix call per cell, with current index and value
    """
    i = 1 # row
    while i < n_rows:
        j = 1 # column
        while j < n_cols:
                
            result = []
            
            insert_score = dynamic_matrix[i-1][j-1] + substitution_matrix[seq1[j-1]][seq2[i-1]]
            result.append(insert_score)
            
            rowgap_score = dynamic_matrix[i-1][j] - penalty
            result.append(rowgap_score)
        
            colgap_score = dynamic_matrix[i][j-1] - penalty
            result.append(colgap_score) 
            
            max_value = max(result)
            dynamic_matrix[i][j] = max_value
            
            WriteTraceback(traceback_matrix, max_value, result, i, j)
            
            j += 1
        i += 1 

############################################################
### 03 - traceback function  
        
def Traceback(seq1, seq2, traceback_matrix):
    """ Trace back decision from evolutionary calculation
    starting from max row and max column, until "•" is found ("•" is in [0][0])
    '↖' = writing the current char from each sequence into according result
    "←" = aligned seq1 gets current char, aligned seq2 gets '-'
    else =  aligned seq2 gets current char, aligned seq1 gets '-'
    after writing jump to the next cell, according to decision
    """          
    i = len(seq2)
    j = len(seq1)
    
    result_seq1 = ''
    result_seq2 = ''
               
    while traceback_matrix[i][j] != "•":
        
        if traceback_matrix[i][j] == '↖' :            
            result_seq1 = "".join((seq1[j-1], result_seq1))
            result_seq2 = "".join((seq2[i-1], result_seq2))            
            i -= 1
            j -= 1        
            
        elif traceback_matrix[i][j] == "←" :            
            result_seq1 = "".join((seq1[j-1], result_seq1))
            result_seq2 = "".join(('-', result_seq2))              
            j -= 1
            
        else:    
            result_seq1 = "".join(('-', result_seq1))
            result_seq2 = "".join((seq2[i-1], result_seq2))       
            i -= 1
            
    return(result_seq1,result_seq2)
 
############################################################
### 04 - substitution matrix from literature

def CreateSubMatrix():
    """ Substitution matrix
    Panda datastructure. the calculation process can directly access 
    nucleotides combination in the panda index
    Based on literature for scoring scheme:
    same nucleotide = 5, indel = -2
    return matrix
    """
    nucleotides = ['A','C','G','T']
    rating =    {'A': [5,-2,-2,-2],
                'C': [-2,5,-2,-2],
                'G':  [-2,-2,5,-2],
                'T':  [-2,-2,-2,5]}
    
    S = pd.DataFrame(rating, index=nucleotides)
    return(S)

######################################
### 10 - Main function

def AlignByDP(Input):
    """ Align sequence pairs
    function:
        takes list(tuple(str,str) as input, containing sequence pairs
        per pair calculate evolutionary score, store decision
        traceback the decision and write aligned sequences
        return the aligned pairs in dict(tuple(int,int) : tuple(str,str)) 
            with tuple(int,int) being the index of the pair and
            tuple(str,str)) being the sequence pair
    scoring:
        Based on Subsitution matrix and
        penalty for a gap is 6, based on literature
    """
    S = CreateSubMatrix()
    
    d = defaultdict(dict)
    n = 0
    while n < len(Input):
        m = n + 1
        while m < len(Input):
            seq1 = Input[n][1]
            seq2 = Input[m][1]
            
            num_cols = len(seq1) + 1
            num_rows = len(seq2) + 1
            
            penalty = 6
            
            D = CreateDynamicMatrix(num_cols, num_rows, penalty)
            T = CreateTracebackMatrix(num_cols, num_rows)
            
            FillMatrices(D, T, S, num_rows, num_cols, seq1, seq2, penalty)
            
            seq1_paired, seq2_paired = Traceback(seq1, seq2, T)
            
            d[(n+1,m+1)] = (seq1_paired, seq2_paired)
    
            m += 1
        n += 1
    return(d)
