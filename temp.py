# -*- coding: utf-8 -*-

# temp stuff

test = {(1,2) : ('AAACATCCAAACACCA——ACCCCAG-',
'ACCAAACCTGTCCCCATCTAACACCA'),
(1,3) : ('AAACATCCAAAC—ACCAACCCCAG-',
'AAT-ACCCAACTCGACCTACACCAA'),
(2,3) : ('ACCAAACCTGTCCCCATCTAACACCA',
'A—ATACCCAACTCGACCTA-CACCAA')}


1 mit 2
1 mit 3
2 mit 3

i = 0
y = i+1

cycle through couples i mit y += 1 until y = max(einträge)
then i += 1


oops = [' \tGibbon  ACTATACCCA CCCAACTCGA CCTACACCAA TCCCCACATA GCACACAGAC CAACAACCTC ']

for i in oops:
    if i == '\\':
        raise InputError(oops,"malformed input") 
    elif i != ' ':
        break
print(oops)

oops[1]