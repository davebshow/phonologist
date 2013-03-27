from fmatrixutils import build_fmatrix
import json
FM = build_fmatrix()

fmatrixdict = {}

for feature in FM:
	fmatrixdict[feature] = FM[feature]

json.dump(fmatrixdict,open("dictobj.txt","w"))

