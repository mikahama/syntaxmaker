#encoding: utf-8
from syntaxmaker.syntax_maker import *
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

print vp
"""
vp = create_verb_pharse("uneksia")
subject = create_phrase("NP", "rantaleijona", {u"PERS": "3", u"NUM": "PL"})
dobject = create_phrase("NP", "aalto", {u"PERS": "3", u"NUM": "PL"})
dobject.components["attribute"] = create_phrase("AP", "korkea")
dobject.components["attribute"].components["attribute"] = create_phrase("AdvP", "erittäin")
vp.components["subject"] = subject
vp.components["dir_object"] = dobject
turn_vp_into_prefect(vp)
turn_vp_into_passive(vp)
set_vp_mood_and_tense(vp, tense="PAST")
print(str(vp))