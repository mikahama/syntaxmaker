Syntax maker
=======

[![Build Status](https://travis-ci.com/mikahama/syntaxmaker.svg?branch=master)](https://travis-ci.com/mikahama/syntaxmaker) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3483626.svg)](https://doi.org/10.5281/zenodo.3483626)

The tool NLG tool for Finnish by [Mika Hämäläinen](https://mikakalevi.com)

Syntax maker is the natural language generation tool for generating syntactically correct sentences in Finnish automatically. The tool is especially useful in the case of Finnish which has such a high diversity in its morphosyntax. All you need to know are the lemmas and their parts-of-speech and syntax maker will take care of the rest.

For instance, just throw in words `rantaleijona`, `uneksia`, `korkea` and `aalto` and you will get `rantaleijonat uneksivat korkeista aalloista`. So you will get the morphology right automatically! Don't believe me? [Just take a look at this tutorial to find out how.](https://github.com/mikahama/syntaxmaker/wiki/Creating-a-sentence,-the-basics)

# Installing
Run

    pip install syntaxmaker
    python -m uralicNLP.download -l fin

After installing it, go to [Creating a sentence, the basics](https://github.com/mikahama/syntaxmaker/wiki/Creating-a-sentence,-the-basics) for a quick start guide.

A good source of example code with the expected output can be found in [the Travis test file](https://github.com/mikahama/syntaxmaker/blob/master/travis_test.py).

Don't forget to [read the Wiki](https://github.com/mikahama/syntaxmaker/wiki) for more instructions.

# Cite

If you use Syntax Maker in any academic publication, please cite it as follows:

Hämäläinen, Mika and Rueter, Jack  2018.  [Development of an Open Source Natural Language Generation Tool for Finnish](http://aclweb.org/anthology/W18-0205).  In *Proceedings of the Fourth International Workshop on Computational Linguistics of Uralic Languages*, 51–58.

# More information?

Just go ahead and [take a look at the wiki](https://github.com/mikahama/syntaxmaker/wiki) or my [blog post about Syntax maker](https://mikalikes.men/create-finnish-sentences-computationally-in-python-nlg/).
