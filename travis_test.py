#encoding: utf-8
import unittest
from syntaxmaker.syntax_maker import *
import codecs
import copy

class TestFSTS(unittest.TestCase):

    def setUp(self):
        vp = create_verb_pharse("uneksia")
        subject = create_phrase("NP", "rantaleijona", {u"PERS": "3", u"NUM": "PL"})
        dobject = create_phrase("NP", "aalto", {u"PERS": "3", u"NUM": "PL"})
        dobject.components["attribute"] = create_phrase("AP", "korkea")
        dobject.components["attribute"].components["attribute"] = create_phrase("AdvP", "erittäin")
        vp.components["subject"] = subject
        vp.components["dir_object"] = dobject
        self.vp = vp

    def test_sentence(self):
        vp = copy.deepcopy(self.vp)
        self.assertEqual(str(vp) , "rantaleijonat uneksivat erittäin korkeista aalloista")
    def test_sentence_pass(self):
        vp = copy.deepcopy(self.vp)
        turn_vp_into_passive(vp)
        self.assertEqual(str(vp) , "uneksitaan erittäin korkeista aalloista")
    def test_sentence_neg(self):
        vp = copy.deepcopy(self.vp)
        negate_verb_pharse(vp)
        self.assertEqual(str(vp) , "rantaleijonat eivät uneksi erittäin korkeista aalloista")
    def test_prefect(self):
        vp = copy.deepcopy(self.vp)
        turn_vp_into_prefect(vp)
        self.assertEqual(str(vp) , "rantaleijonat ovat uneksineet erittäin korkeista aalloista")
    def test_prefect_pass(self):
        vp = copy.deepcopy(self.vp)
        turn_vp_into_prefect(vp)
        turn_vp_into_passive(vp)
        self.assertEqual(str(vp) , "on uneksittu erittäin korkeista aalloista")
    def test_pot(self):
        vp = copy.deepcopy(self.vp)
        set_vp_mood_and_tense(vp, mood="POTN")
        self.assertEqual(str(vp) , "rantaleijonat uneksinevat erittäin korkeista aalloista")

    def test_cond(self):
        vp = copy.deepcopy(self.vp)
        set_vp_mood_and_tense(vp, mood="COND")
        self.assertEqual(str(vp) , "rantaleijonat uneksisivat erittäin korkeista aalloista")

    def test_imp(self):
        vp = copy.deepcopy(self.vp)
        set_vp_mood_and_tense(vp, mood="IMPRT")
        self.assertEqual(str(vp) , "uneksikoon erittäin korkeista aalloista")

    def test_quest(self):
        vp = copy.deepcopy(self.vp)
        turn_vp_into_question(vp)
        self.assertEqual(str(vp) , "uneksivatko rantaleijonat erittäin korkeista aalloista")

    def test_rela(self):
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
        self.assertEqual(str(vep) , "mies, jota orava, jota kissa vaanii, katsoo, juoksee sillan alla")

    def test_copula_pl(self):
        vp = create_copula_phrase()
        subject = create_phrase("NP", "koira", {u"NUM": "PL"})
        predicative = create_phrase("NP", "eläin")
        vp.components["subject"] = subject
        vp.components["predicative"] = predicative
        self.assertEqual(str(vp) , "koirat ovat eläimiä")

    def test_copula_sg(self):
        vp = create_copula_phrase()
        subject = create_phrase("NP", "koira", {u"PERS": "3", u"NUM": "SG"})
        predicative = create_phrase("NP", "eläin")
        vp.components["subject"] = subject
        vp.components["predicative"] = predicative
        self.assertEqual(str(vp) , "koira on eläin")

    def test_adpos(self):
        vp = create_copula_phrase()
        subject = create_phrase("NP", "koira", {u"PERS": "3", u"NUM": "SG"})
        predicative = create_phrase("NP", "eläin")
        adp = create_adposition_phrase("ilman", predicative)
        vp.components["subject"] = subject
        add_advlp_to_vp(vp, adp)
        self.assertEqual(str(vp) , "koira on ilman eläintä")

    def test_palce_name(self):
        vp = create_copula_phrase()
        subject = create_phrase("NP", "koira", {u"PERS": "3", u"NUM": "SG"})
        predicative = create_phrase("NP", "Venäjä")
        vp.components["subject"] = subject
        add_advlp_to_vp(vp, predicative, place_type="in")
        self.assertEqual(str(vp) , "koira on Venäjällä")



if __name__ == '__main__':
    unittest.main()

