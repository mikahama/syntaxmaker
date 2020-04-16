from .syntaxmaker import *

def convert_UD(UD_structure):
	nodes = UD_structure.find()
	phrases = [_node_to_phrase(x) for x in nodes]


def _node_to_phrase(UD_node):
	pos = UD_node.upostag
	if pos == "NOUN" or pos =="PROPN":
		return create_noun_phrase(UD_node.lemma, morphology=_noun_morphology(UD_node.feats))
	elif pos == "ADJ":
		return create_adjective_phrase(UD_node.lemma, morphology=_noun_morphology(UD_node.feats))
	elif pos == "ADV":
		return create_adverb_phrase(UD_node.lemma, morphology=_noun_morphology(UD_node.feats))
	elif pos == "VERB":
		pass
	elif pos == "ADP":
		return create_adposition_phrase(UD_node.lemma, np=None)
	elif pos == "AUX":
		pass
	elif pos == "CCONJ":
		pass
	elif pos == "DET":
		pass
	elif pos == "NUM":
		pass
	elif pos == "PART":
		pass
	elif pos == "PRON":
		pass
	elif pos == "SCONJ":
		pass
	elif pos == "PUNCT" or pos == "SYM" or pos == "X" or pos == "INTJ":
		return create_phrase("GENERIC_P", UD_node.lemma)

def _noun_morphology(UD_node):
	ud_morphs = UD_node.feats.split("|")
	morphology = {}
	psor_n = None
	psor_p = None
	for ud_morph in ud_morphs:
		if ud_morph.startswith("Case="):
			morphology["CASE"] = ud_morph.replace("Case=", "")
		elif ud_morph == "Number=Sing":
			morphology["NUM"] = "Sg"
		elif ud_morph == "Number=Plur":
			morphology["NUM"] = "Pl"
		elif "Number[psor]" in ud_morph:
			if "Sing" in ud_morph:
				psor_n = "Sg"
			else:
				psor_n = "Pl"
		elif "Person[psor]" in ud_morph:
			psor_p = ud_morph[-1]
		elif ud_morph == "Degree=Cmp":
			morphology["DEGREE"] = "Comp"
		elif ud_morph == "Degree=Sup":
			morphology["DEGREE"] = "Superl"
	if psor_n is not None and psor_p is not None:
		morphology["POSS"] = "Px" + psor_n + psor_p
	return morphology








