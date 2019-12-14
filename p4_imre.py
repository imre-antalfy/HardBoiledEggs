# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 08:13:34 2019

@author: Imre Antalfy
"""
# import
from collections import defaultdict
import string

# data from p3

#P3 = [[0.0, 1.2518678603517923, 1.0506698704057822,], 
#      [1.2518678603517923, 0.0, 2.747671234597231], 
#      [1.0506698704057822, 2.747671234597231, 0.0]]
#
#type(P3)

P3 = [[0.0,17.0,21.0,31.0,23.0, 1000.0],
      [17.0,0.0,30.0,34.0,21.0, 1000.0],
      [21.0,30.0,0.0,28.0,39.0, 1000.0],
      [31.0,34.0,28.0,0.0,43.0, 1000.0],
      [23.0,21.0,39.0,43.0,0.0, 1000.0],
      [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 0.0]]



################################
### input functions
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

### calc functions

def InputToDict(Input):
    """ Convert the unique evolutionary distances from the input
        matrix into a dicionary, having each combination possible as a key
        ex. dict{a: {b: value, c: value}, b: {c: value}}
    """
    d = defaultdict(dict)
    alph = string.ascii_lowercase
    
    i = 0
    while i < len(Input):
        j = i+1
        while j < len(Input):  
            d[alph[i]][alph[j]] = Input[i][j]
            j += 1     
        i += 1
    return(d)


def MinEvolDist(dictionary):
    """ find the the key pairing with the minimal distance
    """
    tiny_dist = 40 #change to 31 again
    tiny_key = ""
    for key1, value in dictionary.items():
        for key2, dist in value.items():
            if dist < tiny_dist:
                tiny_dist = dist
                tiny_key = key1, key2
    return(tiny_dist, tiny_key) #to include
    
#def UpdateMatrix(dictionary):

    
    

    
    


################################
### Mainfunctions
CheckInput(P3)
evol_dict = InputToDict(P3)


########################################
# get mindistance and key
Min_dist, Min_key = MinEvolDist(evol_dict)

# delete minimum key
del evol_dict[Min_key[0]][Min_key[1]]

# del empty entries
for key in list(evol_dict.keys()):
    if evol_dict[key] == {}:
        del evol_dict[key]


# write current key 
Min_key_str = '(' + Min_key[0] + ',' + Min_key[1] + ')' 

print(Min_key_str)

# update matrix with new distances
# we need a,c to b, as a and c are out of the picture

if Min_key[0] in evol_dict.keys():
    # if items are outside of the first dict
    for upkey in evol_dict[Min_key[0]].keys(): # hier auch eine liste einfügen?
    
        if Min_key[1] in evol_dict.keys():
    
            evol_dict[Min_key_str][upkey] = (evol_dict[Min_key[0]][upkey]+
                                             evol_dict[Min_key[1]][upkey] )/2
    
        # if items are in first and second dict
        else:
           
            evol_dict[Min_key_str][upkey] = (evol_dict[Min_key[0]][upkey]+
                                             evol_dict[upkey][Min_key[1]] )/2
            
            del evol_dict[upkey][Min_key[1]]
                 
# If items to merge are in the second dict
# elif Min_key[0] not in evol_dict.keys(): # ich glaube dieses if hält nicht immer
else:  
    for upkey in list(evol_dict.keys()):
    
        evol_dict[upkey][Min_key_str] = (evol_dict[upkey][Min_key[0]]+
                                         evol_dict[upkey][Min_key[1]] )/2   
        
        del evol_dict[upkey][Min_key[0]]
        del evol_dict[upkey][Min_key[1]]
        result = '(' + upkey + ',' + Min_key_str + ')'
        
# das könnte man echt noch schöner machen, nach oben... ... ...
# matrix delete loop
for upkey in list(evol_dict[Min_key[0]]):
    del evol_dict[Min_key[0]][upkey]

if Min_key[1] in evol_dict.keys():  
    for upkey in list(evol_dict[Min_key[1]]):
        del evol_dict[Min_key[1]][upkey]     

# del empty entries
for key in list(evol_dict.keys()):
    if evol_dict[key] == {}:
        del evol_dict[key]
   