# -*- coding: utf-8 -*-

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
    preparation for process, del empty lines, split lines
    returns list of lines
    """
    TSeqs = SeqFile.splitlines() 
    TSeqs = list(filter(None,TSeqs))
    return(TSeqs)  

def CheckLabel(Line): 
    """ Checking space before label
    only whitespace allowed, no tabs
    """           
    for i in Line:
        if i == '\t': #can't detect leading tabs, stops at the first \ 
            raise InputError(Line,"malformed input") 
        elif i != ' ':
            break

def CheckSeq(Seq):
    """ Checking seq
    only allowed chars in Seq are A,C,G,T. if Seq differs, raise an error
    """
    OkNucleo = ("A", "C", "G", "T")
    for i in Seq:
        if i not in OkNucleo:
            raise InputError(Seq,"malformed input")          
    
def ProcessLine(TidyLine):
    """ Processing Line
    function to process one line by itself, remove >, split by whistespace, 
    concatonate sequence from splits, stroring sequence in PLine[1]
    raise error if no >, only one string in line or seq is violated
    return label and seq
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
### 02 - Main function

def ParseSeqFile(SeqFile):
    """ parse file and load into list[tuple(string,string)]
    """
    TidyFile = TidyLines(SeqFile)
    
    result = []

    for line in TidyFile:
        t = ( ProcessLine(line) )
        result.append(t)
    return(result)

############################################################
### 03 - Read the file - call 
  
print( ParseSeqFile( rSeqFile("sequence.txt") ) )

