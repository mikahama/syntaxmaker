__author__ = 'mikahama'
from head import Head
import copy
import re

class Phrase:
    def __init__(self, head, structure, morphology={}):
        self.parent = None
        self.head = Head(head, structure["head"])
        self.components = copy.deepcopy(structure["components"])
        if self.components is None:
            self.components = {}
            self.order = ["head"]
        else:
            self.order = copy.deepcopy(structure["order"])
        if "agreement" in structure:
            self.agreement = copy.deepcopy(structure["agreement"])
        else:
            self.agreement = {}
        if "governance" in structure:
            self.governance = copy.deepcopy(structure["governance"])
        else:
            self.governance = {}
        self.morphology = copy.deepcopy(morphology)

    def resolve_agreement(self):
        forms = {}
        for key in self.agreement:
            if key == "parent":
                morphology = self.parent.morphology
            elif key.startswith("parent->"):
                key_p = key[8:]
                morphology = self.parent.components[key_p].morphology
            else:
                morphology = self.components[key].morphology
            for agreement_type in self.agreement[key]:
                forms[agreement_type] = morphology[agreement_type]
        return forms

    def to_string(self, received_governance = {}):
        self.morphology.update(received_governance)
        string_representation = ""
        for item in self.order:
            if item == "head":
                head_word = self.head.get_form(self.morphology, self.resolve_agreement())
                string_representation = string_representation + " " + head_word
            else:
                phrase = self.components[item]
                if type(phrase) is str or type(phrase) is unicode:
                    #Data not set
                    pass
                else:
                    phrase.parent = self
                    governance = {}
                    if item in self.governance:
                        governance = self.governance[item]
                    string_representation = string_representation + " " + phrase.to_string(governance)
        return string_representation.strip()

    def __str__(self):
        text = self.to_string()
        #remove multiple spaces
        text = re.sub("\s\s+", " ", text)
        #remove spaces before punctuation
        text = self.__remove_spaces_punct__(text)
        return text.strip()

    def __remove_spaces_punct__(self, text):
        puncts = ".,;:?!"
        for punct in puncts:
            if " "+punct in text:
                text = text.replace(" " + punct, punct)
        return text
