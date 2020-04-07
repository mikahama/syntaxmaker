import os, codecs
import json
from uralicNLP import uralicApi

valence_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'verb_valences_new.json')
valences = json.load(codecs.open(valence_path, "r", encoding="utf-8"))

locative_cases_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'locative_case.json')
locative_cases = json.load(codecs.open(locative_cases_path, "r", encoding="utf-8"))

if not uralicApi.is_language_installed("fin"):
	print("Finnish morphology is missing\nStarting download... (this should only happen once)")
	uralicApi.download("fin")

class ValencyException(Exception):
    pass