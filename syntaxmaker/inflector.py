# -*- coding: utf-8 -*-
__author__ = 'Mika Hämäläinen'

import os
from . import pronoun_tool
import sys
from uralicNLP import uralicApi

if (sys.version_info > (3, 0)):
    # Python 3
    new_python = True
    from itertools import filterfalse as ffilter
else:
    # Python 2
    new_python = False
    from itertools import ifilterfalse as ffilter


case_suffixes ={"PAR":"A", "NOM": "","GEN":"n","ESS":"nA", "TRA": "ksi", "INE": "ssA", "ELA": "stA", "ADE": "llA", "ABL": "ltA", "ALL": "lle", "ABE": "ttA", "ILL": "n"}
ei_forms = {"SG1": "en", "SG2":"et","SG3":"ei","PL1":"emme", "PL2":"ette", "PL3":"eivät", "PE4": "ei"}
back_vowels = "aou"
front_vowels = "äöy"
vowels = "aeiouyäö"

def inflect(word, pos, args):
    beginning = ""
    if "|" in word:
        beginning, word = word.rsplit("|",1)
        beginning = beginning.replace("|","")
    if len(args) == 0:
        return beginning + word
    clit =""
    if "CLIT" in args:
        if args["CLIT"] == "KO":
            args["CLIT"] = "QST"
        clit = "+" +args["CLIT"].title()
    if pos == "GENERIC":
        return word
    elif pos == "V":
        if "PERS" in args and args["PERS"] == "4":
            voice = "PSS"
        else:
            voice = "ACT"
        if "MOOD" not in args or args["MOOD"] == "INDV":
            args["MOOD"] = "IND"
        if args["MOOD"] == "POTN":
            args["MOOD"] = "POT"
        if args["MOOD"] != "IND":
            tense = ""
        else:
            if "TENSE" not in args:
                tense = "+Prs"
            elif args["TENSE"] == "PRESENT":
                tense = "+Prs"
            elif args["TENSE"] == "PAST":
                tense = "+Prt"

        if word == "ei":
            ei_form = ei_forms[args["NUM"]+args["PERS"]]
            if "CLIT" in args and args["CLIT"] == "QST":
                ei_form = ei_form + "kö"
            return beginning + ei_form

        if "INF" in args:
            if args["INF"] == "A":
                #syödä, juoda
                return beginning + word
            else:
                #syömään, juomaan
                #omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE="+voice+"][INF="+args["INF"]+"][CASE=ILL]"
                omorfi_query = word + "+V+Act+Inf"+args["INF"].title()+"+Sg+Ill"
        elif "NEG" in args and args["NEG"]:
            #(en) syö, juo...
            if "TEMPAUX"  in args and args["PERS"] == "4" and tense == "+Prs":
                # ei ole syöty
                #omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE=ACT][MOOD="+ args["MOOD"] +"]"+tense+"[NEG=CON]"
                omorfi_query = word+"+V+Pss+"+ args["MOOD"].title() +"+Prt+ConNeg"
            else:
                omorfi_query = word+"+V+"+voice.title()+"+"+args["MOOD"].title()+tense.title()+"+ConNeg"
                #omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE="+voice+"][MOOD="+ args["MOOD"] +"]"+tense+ pers_string+"[NEG=CON]"
        else:
            #syön, juon
            if "TEMPAUX"  in args and args["PERS"] == "4":
                #on syöty
                omorfi_query = word + "+V+Act+"+args["MOOD"].title()+tense+"+Sg3"
                #omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE=ACT][MOOD="+ args["MOOD"] +"]"+tense+"[PERS=SG3]"
            elif "PERS" in args and args["PERS"] == "4":
                #omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE="+voice+"][MOOD="+ args["MOOD"] +"]"+tense+pers_string +clit
                omorfi_query = word + "+V+Pss+"+args["MOOD"].title()+tense+"+Pe4" +clit
            else:
                omorfi_query = word + "+V+"+voice.title()+"+"+ args["MOOD"].title() +tense+ "+" + args["NUM"].title() + args["PERS"]+ clit
                #omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE="+voice+"][MOOD="+ args["MOOD"] +"]"+tense+"[PERS="+args["NUM"]+args["PERS"]+"]" +clit
    elif pos == "PPron":
        #personal pronoun
        if "CASE" in args and args["CASE"] == "Gen":
            args["CASE"] = "ACC"
        if "CASE" in args and args["CASE"] == "TrueGen":
            args["CASE"] = "GEN"
        else:
            args["CASE"] = args["CASE"].upper()
        omorfi_query = word + "+Pron+Pers+"+args["NUM"].title()+args["PERS"]+"+"+ args["CASE"].title() + clit
        #omorfi_query = "[WORD_ID="+word+"][POS=PRONOUN][SUBCAT=PERSONAL][PERS="+args["NUM"]+args["PERS"]+"][NUM="+args["NUM"]+"][CASE="+args["CASE"]+"]"
    elif pos == "PastParticiple":
        #participle, syönyt, syöneet, syöty
        if args["NUM"] == "PE":
            #passive
            #omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE=PSS][MOOD=INDV][TENSE=PAST][PERS=PE4][NEG=CON]"
            omorfi_query = word + "+V+Pss+PrfPrc+Sg+Nom"
        else:
            #active
            num = args["NUM"]
            #omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE=ACT][MOOD=INDV][TENSE=PAST][NUM="+num+"][NEG=CON]"
            omorfi_query = word+"+V+Act+PrfPrc+"+num.title()+"+Nom"
    elif pos == "RelPron":
        case = args["CASE"]
        #omorfi_query = "[WORD_ID="+word+"][POS=PRONOUN][SUBCAT=RELATIVE][NUM="+args["NUM"]+"][CASE="+case+"]"
        omorfi_query = word + "+Pron+Rel+"+args["NUM"].title()+"+" + case.title()
    else:
        degree = ""
        if pos == "N":
            pos = "N"
        elif pos == "N+Prop":
            pass
        elif pos == "Adv":
            if "DEGREE" in args:
                pos = "A"
                args["CASE"] = "Ins"
                args["NUM"] = "Pl"
        else:
            pos = "A"

        if "CASE" not in args:
            args["CASE"] = "NOM"
        else:
            args["CASE"] = args["CASE"].upper()
        if "DEGREE" in args:
            degree = "+" + args["DEGREE"]
        possessive = ""
        if "POSS" in args:
            possessive = "+" + args["POSS"]
        #omorfi_query = "[WORD_ID="+word+"][POS="+pos+"][NUM="+args["NUM"]+"][CASE="+args["CASE"]+"]"
        omorfi_query = word +"+" +pos+ degree +"+" + args["NUM"].title() +"+" + args["CASE"].title() + possessive + clit
    word_form = _filter_generated(uralicApi.generate(omorfi_query, "fin"), word)
    if len(word_form) == 0:
        #Generation failed!
        if pos == "N":
            return inflect(beginning + "|" + word, "N+Prop", args)
        else:
            return beginning + backup_inflect(word, pos, args)
    else:
        return beginning + word_form[0][0]

def _filter_generated(res, lemma):
    if len(res) < 2:
        return res
    for r in res:
        r_as = uralicApi.analyze(r[0], "fin", dictionary_forms=True)
        for r_a in r_as:
            r_a = r_a[0]
            if "+Use/Arch" not in r_a and "+Dial/" not in r_a and r_a.startswith(lemma):
                return [r]

def backup_inflect(word, pos, args):
    if pos == "NOUN" or pos == "ADJECTIVE":
        #Nouns and adjectives
        if pronoun_tool.is_personal_pronoun(word):
            return word
        return standard_nominal_inflection(word, args["CASE"],args["NUM"])
    else:
        return word

def case_harmony(case, word):
    case = case_suffixes[case]
    if "A" in case:
        if has_back_vowels(word):
            return case.replace("A", "a")
        else:
            return case.replace("A", "ä")
    else:
        return case

def has_back_vowels(word):
    word = word[::-1]
    for letter in word:
        if letter in back_vowels:
            return True
        elif letter in front_vowels:
            return False
    return False

def standard_nominal_inflection(noun, case, number):
    if case not in case_suffixes:
        return noun

    last_letter = noun[-1]

    if case == "NOM":
        if number =="SG":
            return noun
        else:
            if last_letter not in vowels:
                return noun + "it"
            else:
                return noun + "t"


    if last_letter not in vowels:
        noun = noun + "i"

    if number == "PL" and noun[-1] == "i":
        if case != "PAR":
            noun = noun[:-1] + "ei"
        else:
            noun = noun[:-1] + "ej"
    elif number =="PL":
        noun = noun + "i"

    if case == "ILL":
        if number == "PL":
            noun = noun + "hi"
        else:
            noun = noun + noun[-1]
    noun = noun + case_harmony(case, noun)
    return noun

