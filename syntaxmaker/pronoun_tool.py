# -*- coding: utf-8 -*-
__author__ = 'mika hämäläinen'


pronouns = {"SG1" : "minä", "SG2" : "sinä", "SG3" : "se", "PL1" : "me", "PL2": "te", "PL3": "ne"}


def pronoun(person, human=True):
    if human and person is "SG3":
        return "hän"
    if human and person is "PL3":
        return "he"
    if person in pronouns:
        return pronouns[person]
    else:
        return None

def is_personal_pronoun(p_pronoun):
    if p_pronoun in pronouns.values():
        return True
    else:
        return False
