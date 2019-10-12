# -*- coding: utf-8 -*-
__author__ = 'Mika Hämäläinen'
import csv
import random
import os

prepositions = {}
postpositions = {}

def load_csv(dictionary, file):

    reader = csv.reader(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", file), 'r'))
    for row in reader:
       k, v = row
       dictionary[k] = v

load_csv(prepositions, "prepositions.csv")
load_csv(postpositions, "postpositions.csv")

def preposition_case(prep):
    if prep in prepositions:
        return prepositions[prep]
    else:
        return None

def postposition_case(post):
    if post in postpositions:
        return postpositions[post]
    else:
        return None

def get_an_adposition():
    if random.choice([True, False]):
        return random.choice(postpositions)
    else:
        return random.choice(prepositions)