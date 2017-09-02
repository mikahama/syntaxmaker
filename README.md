Syntax maker
=======
The tool NLG tool for Finnish by [Mika Hämäläinen](https://mikakalevi.com)

Syntax maker is the natural language generation tool for generating syntactically correct sentences in Finnish automatically. The tool is especially useful in the case of Finnish which has such a high diversity in its morphosyntax. All you need to know are the lemmas and their parts-of-speech and syntax maker will take care of the rest.

For instance, just throw in words `rantaleijona`, `uneksia`, `korkea` and `aalto` and you will get `rantaleijonat uneksivat korkeista aalloista`. So you will get the morphology right automatically! Don't believe me? [Just take a look at this tutorial to find out how.](https://github.com/mikahama/syntaxmaker/wiki/Creating-a-sentence,-the-basics)


# Requirements
1. This tool requires Omorfi, you can download the correct binary version from [http://mikakalevi.com/omorfi](http://mikakalevi.com/omorfi)
2. HFST `pip install hfst` for more instructions, see my post about [HFST and Python](https://mikalikes.men/using-hfst-on-python/).

# Installing
You do `pip install syntaxmaker` to install this library.
After installing it, go to [Creating a sentence, the basics](https://github.com/DiscoveryGroup/syntaxmaker/wiki/Creating-a-sentence,-the-basics) for a quick start guide.

# More information?

Just go ahead and [take a look at the wiki.](https://github.com/mikahama/syntaxmaker/wiki)
