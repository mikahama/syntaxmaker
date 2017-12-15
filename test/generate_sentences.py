#encoding: utf-8
from syntaxmaker.syntax_maker import *
import codecs

f = codecs.open("100verbs.txt", "r", encoding="utf-8")
results = []
for verb in f:
	verb = verb.replace("\n", "")
	vp = create_verb_pharse(verb)
	components= vp.components.keys()
	valency = str(len(components))
	if u"subject" in components:
		vp.components["subject"] = create_phrase("NP", "lehmä")
	if u"dir_object" in components:
		vp.components["dir_object"] = create_phrase("NP", "koira")
	if u"indir_object" in components:
		vp.components["indir_object"] = create_phrase("NP", "kissa")
	phrase = vp.to_string()
	results.append([verb, phrase.decode('utf-8'), valency])

fo = codecs.open("results.csv", "w", encoding="utf-8")
for result in results:
	fo.write(";".join(result) + "\n")
fo.close()
