# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 00:40:47 2019

@author: Imre Antalfy
"""
i= 10

def RemoveOne(a):
    a -= 1
    if a > 0:
        print(a)
        RemoveOne(a)
    else:
        return()
    

if __name__ == "__main__":

    
    RemoveOne(i)