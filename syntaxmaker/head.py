#encoding: utf-8
__author__ = 'Mika Hämäläinen'
from . import inflector

class Head:
    def __init__(self, head, pos):
        self.lemma = head
        self.pos = pos

    def get_form(self, governance, agreement):
        if self.lemma is None:
            return ""
        governance.update(agreement)
        return inflector.inflect(self.lemma, self.pos, governance)

    def __str__(self):
        return self.lemma
