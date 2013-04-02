# -*- encoding: utf-8 -*-
import csv
import codecs
from phonologist import Words, Syllables, Symbols, Phrases, Token
from collections import OrderedDict

span_vowels = [u"a",u"e",u"i",u"o",u"u"]

csvfile = codecs.open('TEST5.csv','wb') 
csvfile.write(u'\ufeff'.encode('utf8'))
writer = csv.writer(csvfile)

W = Words.loadfile("manolowords.txt")

S = Syllables(W) 

writer.writerow(["Goyo"])
writer.writerow(["Basic Count"])
writer.writerow(['', "Words","Syllables","+Stress(Syllables)","-Stress(Syllables"])

for vow in span_vowels:
	words = sum(W.token_by_symbol(vow).values())
	syllables = sum(S.token_by_symbol(vow).values())
	stressedcount = sum(S.stressed_token_by_symbol(vow).values())
	unstressedcount = sum(S.unstressed_token_by_symbol(vow).values())
	writer.writerow([vow, words, syllables, stressedcount, unstressedcount])

SY = Symbols(S)

writer.writerow(["Environment Count"])
writer.writerow(['',"_V","C_","_C","S_","_S","Pre(WrdBdr)","Post"])

for vow in span_vowels:
	post_vowells = sum(SY.posterior_vowel(vow).values())
	prec_consonants = sum(SY.preceding_consonant(vow).values())
	post_consonants = sum(SY.posterior_consonant(vow).values())
	prec_cons_dict = SY.preceding_consonant(vow)
	if "s" in prec_cons_dict.keys():
		prec_s = prec_cons_dict[ "s" ]
	else:
		prec_s = 0
	post_cons_dict = SY.posterior_consonant(vow)
	if "s" in post_cons_dict.keys():
		post_s = post_cons_dict[ "s" ]
	else:
		post_s = 0
	pre_post_tonic = W.pretonic_postonic_words(vow)
	pre = pre_post_tonic[ "pretonic" ]
	pos = pre_post_tonic[ "postonic"]

	writer.writerow([vow,post_vowells,prec_consonants,post_consonants,prec_s,post_s,pre,pos])

P = Phrases.loadfile('raulphrases.txt').unstressed_syllable_sequence()

digram_dict = {}
for vow in span_vowels:
	di = vow + u"s"
	for phrase in P:
		symbols = Symbols(phrase)
		syl_dict = symbols.digram(di)
		digram_dict.setdefault(di,0)
		digram_dict[di] += syl_dict[di]
	
odigram_dict = OrderedDict(digram_dict.items())
writer.writerow(["Unstressed syllables vS"])
writer.writerow([digram for digram in odigram_dict.keys()])
writer.writerow([freq for freq in odigram_dict.values()])

csvfile.close()