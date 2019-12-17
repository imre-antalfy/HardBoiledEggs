# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:43:07 2019

@author: Imre Antalfy
"""

import numpy as np
import pandas as pd
from collections import defaultdict


P1 = [('Mouse', 'AAACATCCAAACACCAACCCCAG'),
 ('Bovine', 'ACCAAACCTGTCCCCATCTAACACCA'),
 ('Gibbon', 'AATACCCAACTCGACCTACACCAA')]

######################################
### functions

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
                
########################################
### matrix setup function
                
def SetupDynamicMatrix(n_cols, n_rows, penalty):
    """ # open dynamic programming matrix
        # empty integer matrix
        # this keeps track of the score
        # already calculates starting distances
    """
    Matrix = np.zeros(shape=(n_rows,n_cols), dtype=np.int)
 
    # starting values
    for i in range(1, n_rows):
        Matrix[i][0] = Matrix[i-1][0] - penalty
    
    for j in range(1, n_cols):
        Matrix[0][j] = Matrix[0][j-1] - penalty
    
    return(Matrix)

def SetupTracebackMatrix(n_cols, n_rows):
    """
    """
    Matrix = np.full(shape=(n_rows, n_cols), fill_value=" ", dtype=np.str)
    
    Matrix[0][0] = "•"
    for i in range(1, n_rows):
        Matrix[i][0] = "↑"
    
    for j in range(1, n_cols):
        Matrix[0][j] = "←"
    
    return(Matrix)
    
    
### calculation functions
    
def WriteTraceback(traceback_matrix, current_cell, result_list, 
                   index_row, index_col):
    """
    """
    if current_cell == result_list[0]: # case insertion
        traceback_matrix[index_row][index_col] = '↖' 
        
    elif current_cell == result_list[1]: # case gap row
        traceback_matrix[index_row][index_col] =  "↑"
        
    else: #case gap column
        traceback_matrix[index_row][index_col] =  "←"


def FillMatrices(dynamic_matrix, traceback_matrix, substitution_matrix, 
                 n_rows, n_cols, seq1, seq2, penalty):
    """ 
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
            
            # write maxresult
            max_value = max(result)
            dynamic_matrix[i][j] = max_value
            
            # write traceback
            WriteTraceback(traceback_matrix, max_value, result, i, j)
            
            j += 1
        i += 1    
 
### traceback functions    
        
def Traceback(seq1, seq2, traceback_matrix):
    """
    """          
    i = len(seq2)
    j = len(seq1)
    
    result_seq1 = ''
    result_seq2 = ''
               
    while traceback_matrix[i][j] != "•":
        
        if traceback_matrix[i][j] == '↖' :            
            # write from both sequences
            result_seq1 = "".join((seq1[j-1], result_seq1))
            result_seq2 = "".join((seq2[i-1], result_seq2))            
            # jump
            i -= 1
            j -= 1        
            
        elif traceback_matrix[i][j] == "←" :            
            # write only from horizontal sequence, insert - into vertical
            result_seq1 = "".join((seq1[j-1], result_seq1))
            result_seq2 = "".join(('-', result_seq2))              
            # jump
            j -= 1
            
        else:    
            # write only from vertical sequence, insert - into horizontal
            result_seq1 = "".join(('-', result_seq1))
            result_seq2 = "".join((seq2[i-1], result_seq2))       
            # jump
            i -= 1
    return(result_seq1,result_seq2)
        
######################################
### substitution matrix from literature

# now we need substitution matrix
# open blosum 50 matrix (i need to make that nice with the matrix stuff)
# i only need the blosum50 values for ACTG, from literature
nucleotides = ['A','C','G','T']
rating =    {'A': [5,-2,-2,-2],
            'C': [-2,5,-2,-2],
            'G':  [-2,-2,5,-2],
            'T':  [-2,-2,-2,5]}

S = pd.DataFrame(rating, index=nucleotides)

######################################
### Main function - per sequence couple

def AlignByDP(Input):
    """
    """
    d = defaultdict(dict)
    n = 0
    while n < len(P1):
        m = n + 1
        while m < len(P1):
            seq1 = P1[n][1]
            seq2 = P1[m][1]
            
            num_cols = len(seq1) + 1
            num_rows = len(seq2) + 1
            
            penalty = 6
            
            test = SetupDynamicMatrix(num_cols, num_rows, penalty)
            tracetest = SetupTracebackMatrix(num_cols, num_rows)
            
            FillMatrices(test, tracetest, S, num_rows, num_cols, seq1, seq2, penalty)
            
            seq1_paired, seq2_paired = Traceback(seq1, seq2, tracetest)
            
            d[(n+1,m+1)] = (seq1_paired, seq2_paired)
    
            m += 1
        n += 1
    
############################################
### Main Call
    
