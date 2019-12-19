# -*- coding: utf-8 -*-

"""
Created on Mon Dec 6 16:43:07 2019

@author: Imre Antalfy
"""

############################################################
### 00 - exception handling
    
class Error(Exception):
    """ Base class for exceptions in this module.
    """
    pass
    
class InputError(Error):
    """Exception raised for errors in the input.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error  
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
    
############################################################
### O1 - file handling


def rSeqFile(FilePath):
    """Read file
    returns read file as string
    """
    f=open(FilePath, 'r')
    #check if file open
    if f.mode == 'r': 
        return(f.read())

def TidyLines(SeqFile):
    """ Tidying Lines
    preparation for process, delete empty lines, split lines
    returns list of lines
    """
    TSeqs = SeqFile.splitlines() 
    TSeqs = list(filter(None,TSeqs))
    return(TSeqs)  

def CheckLabel(Line): 
    """ Error in label
    only whitespace allowed, no tabs
    if checked label differs, raise an error
    """           
    for i in Line:
        if i == '\t': #can't detect leading tabs, stops at the first \ 
            raise InputError(Line,"malformed input") 
        elif i != ' ':
            break

def CheckSeq(Seq):
    """ Errors in sequence
    Checking sequence for allowed characters in sequence. only A,C,G,T
    if checked sequence differs, raise an error
    """
    OkNucleo = ("A", "C", "G", "T")
    for i in Seq:
        if i not in OkNucleo:
            raise InputError(Seq,"malformed input")          
    
def ProcessLine(TidyLine):
    """ Processing Line
        Function:
    process one line by itself, remove >, split by whistespace, 
    concatonate sequence from splits, storing sequence in PLine[1]
    return label from PLine[0] and sequence from PLine[1]
        Errorhandling:
    raise error if no >, only one string in line or sequence is violated
    
    """
    if not TidyLine.startswith('>'):
        raise InputError(TidyLine,"malformed input")   
        
    PLine = TidyLine.replace('>','')   
    CheckLabel(PLine)
    PLine = PLine.split()
    
    try:
        for element in PLine[2:]:     
            PLine[1] += "".join(element)       
        CheckSeq(PLine[1])   
        return( PLine[0],PLine[1] ) #Line[0] = Label, Line[1] = Seq
    except IndexError:
        raise InputError(PLine,"malformed input") 
        

############################################################
### 10 - Main function

def ParseSeqFile(FilePath):
    """ parsing a given text file containing labels and sequences
    load file, tidy it, process each line in the file
    return the labels and sequences as list[tuple(string,string)]
    """
    SeqFile = rSeqFile(FilePath)
    TidyFile = TidyLines(SeqFile)
    
    result = []

    for line in TidyFile:
        t = ( ProcessLine(line) )
        result.append(t)
    return(result)


