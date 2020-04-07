from . import locative_cases

locative_map = {"external":{"in":"Ade","to":"All","from":"Abl"},"internal":{"in":"Ine","to":"Ill","from":"Ela"}}

def get_locative(noun):
	if noun in locative_cases:
		noun_data = locative_cases[noun]
		if noun_data["Ade"] > noun_data["Ine"]:
			return "external"
		else:
			return "internal"
	else:
		return None

def resolve_locative_case(locative_category, direction):
	return locative_map[locative_category][direction]
