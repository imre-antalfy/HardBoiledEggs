# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 12:45:41 2019

@author: Michele"""

def P2 (file):
    
    """P2: This function takes a text file conatining DNA Sequences, 
    parses the file and returns a dictionary containg the key which shows which sequence has
    been compared to which, as well as the aligned sequences.
    Alignment of sequences through the use of scoring- and tracebackmatrices for each pair."""
    
    import numpy as np
    from P1 import P1          #call function from P1 to get parsed sequence
    Input=P1('p1input.txt')
    
    #check for the correct format--------------------------------------------------
    if type(Input)!=list:
            raise RuntimeError('malformed input : not a list!')
    for part in range(len(Input)):
        if type(Input[part])!=tuple:
            raise RuntimeError('malformed input : not a list of tuples!')
        elif type(Input[part][0])!=str:
            raise RuntimeError('malformed input : not a list of strings inside of tuples!')
        elif type(Input[part][1])!=str:
            raise RuntimeError('malformed input : not a list of strings inside of tuples!')
    
    #define key value pairs--------------------------------------------------------
    key=list(range(len(Input))) 
    key_value_pairs=[]
    
    for i in range(len(Input)):
        seq=list(Input[i])
        seq[0]=key[i]
        key_value_pairs.append(seq)    
    
    #put all sequences into all possible alignment pairs and define key for dict---  
    seq_pairs_to_be_aligned=[]
    for i in range(len(key_value_pairs)):
        for j in range(i + 1, len(key_value_pairs)):
            seq_pairs_to_be_aligned.append((key_value_pairs[i], key_value_pairs[j]))
            
    key=[]
    for i in range(len(seq_pairs_to_be_aligned)):
              key.append(((((seq_pairs_to_be_aligned[i])[0])[0]), (((seq_pairs_to_be_aligned[i])[1])[0])))
            
    #start loop for aligning all possible alignment pairs____________________________________
    aligned_sequences=[]
   
    for i in range(len(seq_pairs_to_be_aligned)):
        x_sequence=(((seq_pairs_to_be_aligned[i])[0])[1])
        y_sequence=(((seq_pairs_to_be_aligned[i])[1])[1])
    
        #Scoring:
        match=5
        mismatch=-2
        deletion=-6
        
        #filling the 1. row/column of the scoring matrix by multiplying the deletion score
        scoring_matrix = np.zeros(((len(x_sequence))+1,(len(y_sequence))+1))
        traceback_matrix = np.zeros(((len(x_sequence))+1,(len(y_sequence))+1))
        
        for i in range(len(x_sequence)+1):
            scoring_matrix[i,0]=i*deletion
        scoring_matrix
        for j in range(len(y_sequence)+1):
            scoring_matrix[0,j]=j*deletion
        
        #fill in scoring matrix and traceback matrix-----------------------------------
        for i in range(1, len(x_sequence)+1): #rowwise loop
            for j in range(1, len(y_sequence)+1):  #columnwise loop
                
                if x_sequence[i-1] == y_sequence[j-1]:  
                    """Match-> value of left up cell + score for a match (+5) gets inserted
                    into scoringmatrix, value of 1 gets insertet into traceback_matrix. 
                    Unless the value is smaller than that of a left or up cell + deletion value (-6)"""
                    from_left_up_cell = scoring_matrix[i-1, j-1] + match
                    from_up_cell = scoring_matrix[i-1, j]+ deletion
                    from_left_cell= scoring_matrix[i, j-1] + deletion
                    if from_left_up_cell >= from_up_cell and from_left_cell: 
                        scoring_matrix[i,j] = scoring_matrix[i-1, j-1] + match
                        traceback_matrix[i, j] = 1 #from left up cell
                    elif from_up_cell >= from_left_up_cell and from_left_cell:
                        scoring_matrix[i,j]= scoring_matrix[i-1, j]+ deletion
                        traceback_matrix[i, j] = 2 #from the upper cell
                    elif from_left_cell > from_left_up_cell and from_up_cell:
                        scoring_matrix[i,j] = scoring_matrix[i, j-1] + deletion
                        traceback_matrix[i, j] = 3  #from the left cell                
                        
                else: 
                    if (scoring_matrix[i-1, j-1] >= scoring_matrix[i-1, j]) and (scoring_matrix[i-1, j-1] >= scoring_matrix[i, j-1]):
                        """Not a Match-> if it's not a match and the value of the left up cell 
                        is bigger than the value of the upper cell AND of the left cell, value
                        of left up cell + score for a mismatch (-2) gets inserted into 
                        scoringmatrix, value of 1 gets insertet into traceback_matrix"""
                        scoring_matrix[i,j] = scoring_matrix[i-1, j-1] + mismatch
                        traceback_matrix[i, j] = 1
                    elif scoring_matrix[i-1, j] >= scoring_matrix[i, j-1]:
                        """Not a Match-> if it's not a match and the value of the upper cell 
                        is bigger than the value of the left cell, value of upper cell + score 
                        for a deletion (-6) gets inserted into scoringmatrix, 
                        value of 2 gets insertet into traceback_matrix"""
                        scoring_matrix[i,j]= scoring_matrix[i-1, j]+ deletion
                        traceback_matrix[i, j] = 2 
                    elif scoring_matrix[i, j-1] > scoring_matrix[i-1, j]:
                        """Not a Match-> if it's not a match and the value of the left cell 
                        is bigger than the value of the upper cell, value of left cell + score 
                        for a deletion (-6) gets inserted into scoringmatrix, value of 3 gets insertet into traceback_matrix"""
                        scoring_matrix[i,j] = scoring_matrix[i, j-1] + deletion
                        traceback_matrix[i, j] = 3  
        
        """Note: Some cells can be reached by two or three different optimal paths
        of equal score: whenever two or more cases are equally optimal, dynamic programming
        implementations usually choose one case arbitrarily. In this example, it was set 
        that the from_left_up cell gets chosen over the from_up_cell which gets chosen over the from_left_cell"""          
                            
        #align sequences---------------------------------------------------------------
        x_sequence_aligned=list()
        y_sequence_aligned=list()
        i=len(x_sequence)
        j=len(y_sequence) 
         
        while i != 0 or j != 0:
            if traceback_matrix[i, j] == 1:
                    x_sequence_aligned.append(x_sequence[i-1])
                    y_sequence_aligned.append(y_sequence[j-1])
                    i=i-1
                    j=j-1
            elif traceback_matrix[i, j] == 2:
                    x_sequence_aligned.append(x_sequence[i-1])
                    y_sequence_aligned.append("-")
                    i=i-1
            else:
                    x_sequence_aligned.append("-")
                    y_sequence_aligned.append(y_sequence[j-1])
                    j=j-1
        
        x_sequence_aligned.reverse()
        y_sequence_aligned.reverse()
        x_sequence_aligned=''.join(x_sequence_aligned)
        y_sequence_aligned=''.join(y_sequence_aligned)
        aligned_sequences.append((x_sequence_aligned,y_sequence_aligned))
    #define dictionary-------------------------------------------------------------  
    global dictionary
    dictionary = dict(zip(key, aligned_sequences))
    return(dictionary)

#call function
#print(P2('p1input.txt'))