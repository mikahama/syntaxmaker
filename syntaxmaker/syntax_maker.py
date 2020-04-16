# -*- coding: utf-8 -*-
__author__ = 'Mika Hämäläinen'
from . import verb_valence
from .phrase import Phrase
import json
import random
from . import pronoun_tool
from . import adposition_tool
import os
from . import noun_tool, ValencyException

auxiliary_verbs = {"voida" : "A",
"saada" : "A",
"alkaa" : "A",
"haluta" : "A",
"ruveta" : "MA",
"saattaa" : "A",
"kehdata": "A",
"jäädä": "MA",
"yrittää": "A",
"unohtaa":"A"}

grammar =""

def load_grammar():
    global grammar
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "grammar.json")
    f = open(path, "r")
    jsonText = f.read()
    f.close()
    grammar = json.loads(jsonText)

load_grammar()

def is_auxiliary_verb(verb):
    if verb in auxiliary_verbs:
        return True
    else:
        return False

def create_verb_pharse(head):
    global grammar
    phrase_type = verb_valence.valency_count(head)
    governance = {}
    dir_obj = {}
    dir_obj[u"CASE"] = verb_valence.most_frequent_case(verb_valence.verb_direct_objects(head))
    governance["dir_object"] = dir_obj
    indir_obj = {}
    indir_obj[u"CASE"] = verb_valence.most_frequent_case(verb_valence.verb_indirect_objects(head))
    governance["indir_object"] = indir_obj

    phrase_structure = grammar["VP"+str(phrase_type)]
    phrase_structure["governance"] = governance
    vp = Phrase(head, phrase_structure)
    vp.morphology["VOICE"] = "ACT"
    return vp

default_np_morphology = {u"CASE": "Nom", u"NUM": "SG", u"PERS": "3"}

def create_phrase(name, head, morphology={}):
    global grammar
    if name in grammar:
        structure = grammar[name]
    else:
        structure = grammar["GENERIC_P"]
    if name == "NP":
        for key in default_np_morphology.keys():
            if key not in morphology:
                morphology[key] = default_np_morphology[key]
    return Phrase(head, structure, morphology)

def create_noun_phrase(head, morphology={}, number=None, case=None):
    if case is not None:
        morphology["CASE"] = case
    if number is not None:
        morphology["NUM"] = number
    return create_phrase("NP", head, morphology=morphology)

def create_adjective_phrase(head, morphology={}, degree=None):
    if degree is not None:
        morphology["DEGREE"] = degree
    return create_phrase("AP", head, morphology=morphology)

def create_personal_pronoun_phrase(person = "1", number = "SG", prodrop=False, human=False):
    if prodrop and person != "3":
        pronoun = None
    else:
        pronoun = pronoun_tool.pronoun(number + person, human=human)
    pp = create_phrase("NP", pronoun, morphology={u"PERS": person, u"NUM": number})
    pp.head.pos = "PPron"
    return pp

def create_copula_phrase(predicative_case=None, predicative_number=None):
    global grammar
    structure = grammar["VP_COPULA"]
    governance = { "predicative" :  {u"CASE" : predicative_case, u"NUM":predicative_number, u"PREDICATIVE":True}}
    structure["governance"] = governance
    vp = Phrase("olla", structure)
    vp.morphology["VOICE"] = "ACT"
    return vp


def negate_verb_pharse(vp):
    aux = create_phrase("GENERIC_P", "ei")
    aux.agreement["parent->subject"] = ["PERS", "NUM"]
    aux.head.pos = "V"
    vp.morphology["NEG"] = True
    vp.components["AUX"] = aux
    head_index = vp.order.index("head")
    vp.order.insert(head_index, "AUX")
    if "dir_object" in vp.governance:
        if vp.governance["dir_object"][u"CASE"] == "Gen" or vp.governance["dir_object"][u"CASE"] == "Nom":
            #Genitive or nomintaive objects to partitive syön kakun/syödään kakku -> en syö kakkua/ei syödä kakkua
            vp.governance["dir_object"][u"CASE"] = "Par"

def turn_vp_into_question(vp):
    if "NEG" in vp.morphology:
        vp.components["AUX"].morphology["CLIT"] = "KO"
        move_front = "AUX"
    else:
        vp.morphology["CLIT"] = "KO"
        move_front = "head"

    vp.order.remove(move_front)
    vp.order.insert(0, move_front)

def add_np_subject_to_vp(vp, np):
    if "subject" not in vp.order:
        raise ValencyException("This verb "+str(vp.head)+" does not accept a subject")
    else:
        vp.components["subject"] = np

def add_np_object_to_vp(vp, np, indirect=False, check_valency=False):
    if not indirect:
        if "predicative" in vp.order:
            vp.components["predicative"] = np
        elif "dir_object"  in vp.order:
            vp.components["dir_object"] = np
        elif check_valency == False:
            vp.order.append("dir_object")
            vp.components["dir_object"] = np
        else:
            raise ValencyException("This verb "+str(vp.head)+" does not accept an object or a predicative")
    else:
        if "indir_object"  in vp.order:
            vp.components["indir_object"] = np
        elif check_valency == False:
            vp.components["indir_object"] = np
            vp.order.append("indir_object")
        else:
            raise ValencyException("This verb "+str(vp.head)+" does not accept an indirect object")


def add_auxiliary_verb_to_vp(vp, aux=None):
    if aux is None or aux not in auxiliary_verbs:
        return
    infinitive = auxiliary_verbs[aux]

    infp = create_phrase("GENERIC_P", vp.head.lemma)
    infp.head.pos = "V"
    infp.morphology["INF"] = infinitive

    vp.components["INF"] = infp
    head_index = vp.order.index("head")
    vp.order.insert(head_index+1, "INF")
    vp.head.lemma = aux

def turn_vp_into_prefect(vp):
    old_verb = vp.head.lemma
    vp.head.lemma = "olla"

    participle = create_phrase("GENERIC_P", old_verb)
    participle.head.pos = "PastParticiple"
    participle.agreement["parent->subject"] = ["NUM"]

    vp.components["Participle"] = participle
    vp.morphology["TEMPAUX"] = True
    head_index = vp.order.index("head")
    vp.order.insert(head_index+1, "Participle")

def set_vp_mood_and_tense(vp, mood="INDV", tense="PRESENT"):
    vp.morphology["MOOD"] = mood
    vp.morphology["TENSE"] = tense

def turn_vp_into_passive(vp):
    subject_p = create_phrase("GENERIC_P", None, {u"PERS": "4", u"NUM": "PE"})
    vp.components["subject"] = subject_p
    if "dir_object" in vp.governance:
        if vp.governance["dir_object"][u"CASE"] == "Gen":
            #Genitive object to nominative: Syön kaukun -> syödään kakku
            vp.governance["dir_object"][u"CASE"] = "Nom"

def add_relative_clause_to_np(np, realtivep, case=None, subject=False):
    component = None
    if subject:
        #e.g. kissa, joka kiipesi puuhun
        component = "subject"
        if case is None:
            case = "Nom"
    #if case is none -> the antecedent of the relative clause will be the object of the verb e.g. talo, jonka näin
    elif case is None:
        #set the relative pronoun at the first free component such as direct object or indirect object
        objs = ["dir_object", "indir_object", "predicative"]
        for obj in objs:
            if obj in realtivep.components and type(realtivep.components[obj]) is not Phrase:
                component = "dir_object"
                break

    if component is None:
        #If can't be added to nowhere else or has a specific case e.g. päivä, jona kävelin kadulla
        component = "relative_pron"
        np.components[component] = "NP"
        np.order.append(component)

    morphology = {"NUM":"SG"}
    if case:
        morphology["CASE"] = case
    morphology["NUM"] = np.morphology["NUM"]
    if subject:
        morphology["PERS"] = np.morphology["PERS"]
    rel_pron = create_phrase("NP", "joka",morphology)
    rel_pron.head.pos = "RelPron"

    realtivep.components[component] = rel_pron
    realtivep.order.remove(component)
    realtivep.order.insert(0, component)

    realtivep.components["comma"] = create_phrase("GENERIC_P", ",")
    realtivep.order.insert(0, "comma")
    realtivep.order.append("comma")

    np.components["relative_attribute"] = realtivep
    np.order.append("relative_attribute")

def add_advlp_to_vp(vp, advlp, place_type=None, default_locative_category="internal"):
    index = 0
    for component in vp.components:
        if component.startswith("AdvlP"):
            index = index + 1
    comp_name = "AdvlP" + str(index)
    if place_type is not None:
        loc = noun_tool.get_locative(advlp.head.lemma) or default_locative_category
        advlp.morphology["CASE"] = noun_tool.resolve_locative_case(loc, place_type)

    vp.components[comp_name] = advlp
    vp.order.append(comp_name)

def create_adposition_phrase(adposition, np=None):
    if adposition is None:
        adposition = adposition_tool.get_an_adposition()
    case = adposition_tool.postposition_case(adposition)
    if case is not None:
        phrase = create_phrase("PostP", adposition)
    else:
        case = adposition_tool.preposition_case(adposition)
        if case is None:
            return None
        phrase = create_phrase("PrepP", adposition)
    phrase.governance["complement"] = {u"CASE": case}
    if np is None:
        np = ""
    phrase.components["complement"] = np
    return phrase

def create_adverb_phrase(head, morphology={}, degree=None):
    if degree is not None:
        morphology["DEGREE"] = degree
    return create_phrase("AdvP", head, morphology=morphology)

def add_possessive_to_np(np, person, number, prodrop=False, human=False, suffix=True):
    if human and person == "3":
        suffix = False
    persp = create_personal_pronoun_phrase(person, number, prodrop=prodrop, human=human)
    persp.morphology["CASE"] = "TrueGen"
    if suffix:
        np.morphology["POSS"] = "Px" + number.title() + person
    if not prodrop:
        np.components["det"] = persp
        np.order.insert(0, "det")




"""
vp = create_verb_pharse("uneksia")
add_auxiliary_verb_to_vp(vp)



subject = create_phrase("NP", "rantaleijona", {u"PERS": "3", u"NUM": "PL"})


dobject = create_phrase("NP", "aalto", {u"PERS": "3", u"NUM": "PL"})
dobject.components["attribute"] = create_phrase("AP", "korkea")

dobject.components["attribute"].components["attribute"] = create_phrase("AdvP", "erittäin")


vp.order.insert(0, "Advl")
advl = {u"CASE": "Ess" }
vp.governance["Advl"] = advl
vp.components["Advl"] = create_phrase("NP","hipsteri",{u"PERS": "3", u"NUM": "PL"})

vp.components["subject"] = subject
vp.components["dir_object"] = dobject

#turn_vp_into_passive(vp)
#negate_verb_pharse(vp)

turn_vp_into_prefect(vp)
set_vp_mood_and_tense(vp, mood="POTN")

turn_vp_into_question(vp)
print(vp.to_string())

np = create_phrase("NP", "kissa")
pp = create_adposition_phrase("ilman", np)
print(pp.to_string())



np1 = create_phrase("NP", "mies")
relp = create_verb_pharse("katsoa")
ppp = create_phrase("NP", "orava")
relpp = create_verb_pharse("vaania")
relpp.components["subject"] = create_phrase("NP", "kissa")
add_relative_clause_to_np(ppp, relpp)

relp.components["subject"] = ppp
add_relative_clause_to_np(np1,relp)

vep = create_verb_pharse("juosta")
vep.components["subject"] = np1

np2 = create_phrase("NP", "silta")
pp = create_adposition_phrase("alla", np2)

add_advlp_to_vp(vep, pp)

print(vep)


"""