# -*- coding: utf-8 -*-

############################################################
# 00 - exception handling
# defining the class Input error, when malformed input occurs ind the 
# read file occurs
############################################################
    
class Error(Exception):
#    Base class for exceptions in this module.
    pass
    
class InputError(Error):
#    Exception raised for errors in the input.
#
#    Attributes:
#        expression -- input expression in which the error occurred
#        message -- explanation of the error  

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
    
############################################################
# O1 - file handling
# functions to read input, tidy it and process input, line by line
############################################################

###
# Read file - function
def rSeqFile(FilePath):
    f=open(FilePath, 'r')
    #check if file open
    if f.mode == 'r': 
        return(f.read())

###
# Tidying data - function
# preparation for process
# del leading whitespace before labels, empty lines and >
def TidySeqs(SeqFile):
    #split by lines
    TSeqs = SeqFile.splitlines() 
    #remove empty rows
    TSeqs = list(filter(None,TSeqs))
    return(TSeqs)

###
# concatonating sequences - function
# the whole sequence will be stored in Line[1]
def ConcatSeqs(Line):
    for element in Line[2:]:
        Line[1] += str(element)

###
#Processing Line - function
def ProcessLine(TidyLine):
    #remove > and strip leading whitespace. 
    #lstrip doesnt work with > infront
    PLine = TidyLine.replace('>','')
    PLine = PLine.split()
    #Concat call, if sequence is split
    ConcatSeqs(PLine)
    #check for malformed sequence
    CheckSeq(PLine[1])
    return( PLine[0],PLine[1] )
    

############################################################   
# Exception handling - function
# check, if sequence only contains A,C,G,T
def CheckSeq(Seq):
    ok_genoms = {"A", "C", "G", "T"}
    genom_diff = ok_genoms.symmetric_difference(Seq)
    # raise error if the diff is anything else in Seq than A,C,T,G
    if not genom_diff.issubset(ok_genoms):
        raise InputError(Seq,"malformed input")
    
############################################################
### Main function

def ParseSeqFile(SeqFile):
    
    #tidy the data
    TidyFile = TidySeqs(SeqFile)
    
    result = []

    #load processed seqs into tuple
    for line in TidyFile:
        t = ( ProcessLine(line) )
        result.append(t)
    print(result)

############################################################
### Read the file - call 
  
ParseSeqFile( rSeqFile("sequence.txt") )



