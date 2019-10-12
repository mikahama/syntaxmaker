# -*- coding: utf-8 -*-
__author__ = 'Mika Hämäläinen'
import hfst
import os
from . import pronoun_tool
import sys

if (sys.version_info > (3, 0)):
    # Python 3
    new_python = True
    from itertools import filterfalse as ffilter
else:
    # Python 2
    new_python = False
    from itertools import ifilterfalse as ffilter

datadir = "/usr/local/share/hfst/fi/"
if os.name == 'nt':
    #Windows
    datadir = "C:\\omorfi\\hfst\\fi\\"

generation_set = os.path.abspath(datadir + "omorfi-omor.generate.hfst")


input_stream = hfst.HfstInputStream(generation_set)
synthetiser = input_stream.read()


case_suffixes ={"PAR":"A", "NOM": "","GEN":"n","ESS":"nA", "TRA": "ksi", "INE": "ssA", "ELA": "stA", "ADE": "llA", "ABL": "ltA", "ALL": "lle", "ABE": "ttA", "ILL": "n"}
ei_forms = {"SG1": "en", "SG2":"et","SG3":"ei","PL1":"emme", "PL2":"ette", "PL3":"eivät", "PE4": "ei"}
back_vowels = "aou"
front_vowels = "äöy"
vowels = "aeiouyäö"

def inflect(word, pos, args):
    for el in args:
        if not new_python and type(args[el]) is unicode:
            args[el] = args[el].encode('utf-8')

    if not new_python and type(word) is unicode:
        word = word.encode('utf-8')
    word = word.replace("|", "")
    if len(args) == 0:
        return word
    if pos == "GENERIC":
        return word
    elif pos == "V":
        if "PERS" in args and args["PERS"] == "4":
            voice = "PSS"
            pers_string = "[PERS=PE4]"
        else:
            voice = "ACT"
            pers_string = ""
        if "MOOD" not in args:
            args["MOOD"] = "INDV"
        if args["MOOD"] != "INDV":
            tense = ""
        else:
            if "TENSE" not in args:
                tense = "[TENSE=PRESENT]"
            else:
                tense = "[TENSE="+args["TENSE"]+"]"
        if "CLIT" in args:
            clit = "[CLIT=" + args["CLIT"] + "]"
        else:
            clit = ""

        if word == "ei":
            ei_form = ei_forms[args["NUM"]+args["PERS"]]
            if "CLIT" in args and args["CLIT"] == "KO":
                ei_form = ei_form + "kö"
            return ei_form

        if "INF" in args:
            if args["INF"] == "A":
                #syödä, juoda
                return word
            else:
                #syömään, juomaan
                omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE="+voice+"][INF="+args["INF"]+"][CASE=ILL]"
        elif "NEG" in args and args["NEG"]:
            #(en) syö, juo...
            if "TEMPAUX"  in args and args["PERS"] == "4" and tense == "[TENSE=PRESENT]":
                # ei ole syöty
                omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE=ACT][MOOD="+ args["MOOD"] +"]"+tense+"[NEG=CON]"
            else:
                omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE="+voice+"][MOOD="+ args["MOOD"] +"]"+tense+ pers_string+"[NEG=CON]"
        else:
            #syön, juon
            if "TEMPAUX"  in args and args["PERS"] == "4":
                #on syöty
                omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE=ACT][MOOD="+ args["MOOD"] +"]"+tense+"[PERS=SG3]"
            elif "PERS" in args and args["PERS"] == "4":
                omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE="+voice+"][MOOD="+ args["MOOD"] +"]"+tense+pers_string +clit
            else:
                omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE="+voice+"][MOOD="+ args["MOOD"] +"]"+tense+"[PERS="+args["NUM"]+args["PERS"]+"]" +clit
    elif pos == "PPron":
        #personal pronoun
        if args["CASE"] == "Gen":
            args["CASE"] = "ACC"
        else:
            args["CASE"] = args["CASE"].upper()
        omorfi_query = "[WORD_ID="+word+"][POS=PRONOUN][SUBCAT=PERSONAL][PERS="+args["NUM"]+args["PERS"]+"][NUM="+args["NUM"]+"][CASE="+args["CASE"]+"]"
    elif pos == "PastParticiple":
        #participle, syönyt, syöneet, syöty
        if args["NUM"] == "PE":
            #passive
            omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE=PSS][MOOD=INDV][TENSE=PAST][PERS=PE4][NEG=CON]"
        else:
            #active
            num = args["NUM"]
            omorfi_query = "[WORD_ID="+word+"][POS=VERB][VOICE=ACT][MOOD=INDV][TENSE=PAST][NUM="+num+"][NEG=CON]"
    elif pos == "RelPron":
        case = args["CASE"].upper()
        if case == "NOM":
            if args["NUM"] == "SG":
                return "joka"
            else:
                return "jotka"
        omorfi_query = "[WORD_ID="+word+"][POS=PRONOUN][SUBCAT=RELATIVE][NUM="+args["NUM"]+"][CASE="+case+"]"
    else:
        if pos == "N":
            pos = "NOUN"
        else:
            pos = "ADJECTIVE"

        if "CASE" not in args:
            args["CASE"] = "NOM"
        else:
            args["CASE"] = args["CASE"].upper()
        omorfi_query = "[WORD_ID="+word+"][POS="+pos+"][NUM="+args["NUM"]+"][CASE="+args["CASE"]+"]"
    #word_form = old_generator(omorfi_query)
    word_form = new_generator(omorfi_query)
    if word_form is None:
        #Generation failed!
        return backup_inflect(word, pos, args)
    else:
        return word_form

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

def new_generator(analysis):
    results = synthetiser.lookup(analysis)
    if len(results) != 0:
        word = results[0][0]
        return word
    else:
        return None

def old_generator(omorfi_query):
    result = os.popen("echo \"" + omorfi_query + "\" | omorfi-generate.sh").read()
    word_form = result.split("\t")[1]
    if "[" in word_form:
        return None
    else:
        return word_form

def process_result_vector(vector):
    results = []
    for entry in vector:
        if len(entry) < 2:
            continue
        weight = entry[0]
        string = ''.join(ffilter(libhfst.FdOperation.is_diacritic, entry[1]))
        results.append((string, weight))
    return results
