# -*- encoding: utf-8 -*-
import csv
import codecs
from phonologist import Words, Nsyllables
from collections import OrderedDict

span_vowells = ["a","e","i","o","u"]


csvfile = codecs.open('beta.csv','wb') 
csvfile.write(u'\ufeff'.encode('utf8'))
writer = csv.writer(csvfile)

W = Words("VisualTest.txt")

S = Nsyllables(W) 

writer.writerow(["Elika"])
writer.writerow(["Basic Count"])
writer.writerow([" ", "Words","Syllables","+Stress","-Stress"])

for vow in span_vowells:
	words = sum(W.return_tokens_words(vow).values())
	syllables = sum(S.return_tokens_sylls(vow).values())
	stressedcount = sum(S.stressed_target_sylls(vow).values())
	unstressedcount = sum(S.unstressed_target_sylls(vow).values())
	writer.writerow([vow, words, syllables, stressedcount, unstressedcount])

writer.writerow([" "])
writer.writerow([" "])
writer.writerow(["Environment Count"])
writer.writerow([" ","_V","C_","_C","S_","_S","Pre","Post"])
for vow in span_vowells:
	post_vowells = sum(S.posterior_vowell(vow).values())
	prec_consonants = sum(S.preceding_consonant(vow).values())
	post_consonants = sum(S.posterior_consonant(vow).values())
	prec_cons_dict = S.preceding_consonant(vow)
	if "s".encode('utf-8') in prec_cons_dict.keys():
		prec_s = prec_cons_dict[ "s".encode('utf-8')]
	else:
		prec_s = 0
	post_cons_dict = S.posterior_consonant(vow)
	if "s".encode('utf-8') in post_cons_dict.keys():
		post_s = post_cons_dict[ "s".encode('utf-8')]
	else:
		post_s = 0
	pre_post_tonic = W.pretonic_postonic_words(vow)
	pre = pre_post_tonic[ "pretonic" ]
	pos = pre_post_tonic[ "postonic"]
	writer.writerow([vow,post_vowells,prec_consonants,post_consonants,prec_s,post_s,pre,pos])







###########################################
#sword_dict = W.stressed_frequency()
#osword_dict = OrderedDict(sword_dict.items())

#writer.writerow([word.encode('utf-8') for word in osword_dict.keys()])
#writer.writerow([wfreq for wfreq in osword_dict.values()])


#mydict = W.preceding_symbol("e")
#print mydict

#writer.writerow(["Symbols preceding : e"])
#for char,freq in mydict.items():

#	writer.writerow([char.encode('utf8'),freq])

csvfile.close()