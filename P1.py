# -*- coding: utf-8 -*-

# P1 module of programming class project

#open .txt and read content
f=open("sequence.txt", "r")
#check if file open
if f.mode == 'r': 
    all_seqs =f.read()


#opening list
genomic_list = ["Label","Sequence"]

#as long as > in read data, try to export
if all_seqs.count(">") > 1:
    
    while True:
    
        if all_seqs[0] == ">":
            
            if all_seqs[1].isupper():
                
                label_seq_R = all_seqs.split(" ",1) #split at next ocurring whitespace
                
                #export label
                label = label_seq_R[0]
                label = label.replace(">","")
        
                #export sequence
                seq_R = label_seq_R[1].split("\n",1)
                seq = seq_R[0].replace(" ","")
                
                #EH: check, if sequence is violated
                ok_genoms = {"A", "C", "G", "T"}
                genom_diff = ok_genoms.symmetric_difference(seq)
                if not genom_diff.issubset(ok_genoms):
                    print("malformed input")
                    break
                
                #store data
                t = (label,seq)
                genomic_list.append(t)
                
                print(genomic_list)
                
                #Last sequence reached
                if all_seqs.count(">") == 1: 
                    break
                
                #delete used string parts from main string
                all_seqs = seq_R[1]
                
            elif all_seqs[1].isspace():
                #delete whitespace before label
                all_seqs = all_seqs[0 : 1 : ] + all_seqs[2 :  : ]
            
            #EH: never finding a label
            else:
                print ("malformed input")
                break
                
        elif all_seqs[0] == "\n":
            all_seqs = all_seqs[1 :  : ]
            
#EH: having no > lines in file
elif all_seqs.count(">") == 0:
    print ("malformed input")
