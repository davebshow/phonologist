# -*- encoding: utf-8 -*-
import csv
import codecs
from phonologist import Phonologist
from collections import OrderedDict

span_vowells = ["a","e","i","o","u"]


csvfile = codecs.open('test.csv','wb') 
csvfile.write(u'\ufeff'.encode('utf8'))
writer = csv.writer(csvfile)

PW = Phonologist("words.txt")

PP = Phonologist("phrases.txt").syllabify() 

writer.writerow(["Basic Count"])
writer.writerow([" ", "Words","Syllables","+Stress","-Stress"])

for vow in span_vowells:
	words = sum(PW.return_tokens(vow).values())
	syllables = sum(PP.return_tokens(vow).values())
	stressedcount = sum(PP.stressed_target(vow).values())
	unstressedcount = sum(PP.unstressed_target(vow).values())
	writer.writerow([vow, words, syllables, stressedcount, unstressedcount])

writer.writerow([" "])
writer.writerow([" "])
writer.writerow(["_V","C_","_C","S_","Pre","Post"])









###########################################
sword_dict = PW.stressed_frequency()
osword_dict = OrderedDict(sword_dict.items())

writer.writerow([word.encode('utf-8') for word in osword_dict.keys()])
writer.writerow([wfreq for wfreq in osword_dict.values()])


#mydict = PW.preceding_symbol("e")
#print mydict

#writer.writerow(["Symbols preceding : e"])
#for char,freq in mydict.items():

#	writer.writerow([char.encode('utf8'),freq])

#csvfile.close()