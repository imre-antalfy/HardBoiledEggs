# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 08:13:34 2019

@author: Imre Antalfy
"""

from collections import defaultdict


############################################################
### 00 - input functions
def CheckInput(Input):
    """ Check if input is list(list(float))
    """
    if type(Input) != list:
        raise Exception(Input, "malformed input")
        
    for row in Input:
        if type(row) != list:
            raise Exception(row, "malformed input")
            
        for value in row:
            if type(value) != float:
                raise Exception(value, "malformed input")

def CheckLabels(distance_matrix, label_list):
    """ raise error if more labels than matrix entries
    """
    if len(distance_matrix) != label_lsit:
        raise Exception(label_list,"malformed input")
    

############################################################
### 01 - calc functions

def InputToDict(Input,Labels):
    """ Convert the unique evolutionary distances from the input
        matrix into a dicionary, having each label combo possible as a key
        the keys are directly the genomic types
        ex. dict{Mouse: {Gibbon: value, Human: value}, Gibbon: {Human: value}}
        returns the dict
    """
    d = defaultdict(dict)    
    i = 0
    while i < len(Input):
        j = i+1
        while j < len(Input):  
            d[Labels[i]][Labels[j]] = Input[i][j]
            d[Labels[j]][Labels[i]] = Input[j][i]
            j += 1     
        i += 1
    return(d)


def MinEvolDist(dictionary):
    """ find the the key pairing with the minimal distance
    evolutionary distance cant be longer than 30
    """
    tiny_dist = 31
    tiny_key = ""
    for key1, value in dictionary.items():
        for key2, dist in value.items():
            if dist < tiny_dist:
                tiny_dist = dist
                tiny_key = key1, key2
    return(tiny_key)

def DelEmptyEntries(Dictionary):
    """ delete empty entries in dicts
    """    
    for key in list(Dictionary.keys()):
        if Dictionary[key] == {}:
            del Dictionary[key]

def UpdateMatrix(dictionary):
    """ update the matrix and calculate the new distances
    as long as there are more than two entries in the dict
    search for the minimal key, delete the minmal entry, construct the new key
    for each key in the list, update entries, 
    
    example: new minimal key = (a,b)
        update all entries to resemble the distance from entry to (a,b)
        take mean of both distances = (a,c + b,c)/2
    
    write new distance in both direction intodictionaries
        ex. (a,b):c and c:(a,b) 
    needed, as shile dictionary is used to calculate ditances
    
    return updated dictionary       
    """
    while len(dictionary.values()) != 2:
          
        # get mindistance and key
        min_key_list = MinEvolDist(dictionary)
        
        # delete minimum key in dict entry used for search
        del dictionary[min_key_list[0]][min_key_list[1]]
        del dictionary[min_key_list[1]][min_key_list[0]]
        
        # form new new key
        minimal_key_str = '(' + min(min_key_list) + ',' + max(min_key_list) + ')'
#        minimal_key_str = '(' + min_key_list[0] + ',' + min_key_list[1] + ')'
        
        # update new key
        for key in list(dictionary.keys()): 
            if key != min_key_list[0] and key != min_key_list[1]:

                dictionary[minimal_key_str][key] = (dictionary[min_key_list[0]][key]+
                          dictionary[min_key_list[1]][key] )/2
        
                dictionary[key][minimal_key_str] = (dictionary[min_key_list[0]][key]+
                          dictionary[min_key_list[1]][key] )/2
        # delete used keys
                del dictionary[min_key_list[0]][key]
                del dictionary[min_key_list[1]][key]
                
                del dictionary[key][min_key_list[0]]
                del dictionary[key][min_key_list[1]]
         
        DelEmptyEntries(dictionary)    
    return(dictionary)

################################
### Mainfunctions
    
def Cluster(distance_matrix, labels):
    """ Clustering each genomic type
    also taking genomix labels as a list to represent dendrogram
    return a string, with genomic pairs in brackets, resembling a dendrogram
    """
    CheckInput(distance_matrix)
    
    evol_dict = InputToDict(distance_matrix, labels)
    evol_dict = UpdateMatrix(evol_dict)
    result = '(' + min(evol_dict.keys()) + ',' + max(evol_dict.keys()) + ')'
    return(result)
