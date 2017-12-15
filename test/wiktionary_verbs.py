import codecs
import random
f = codecs.open("fiwiktionary-latest-pages-articles.xml", "r", encoding="utf-8")
seen_verb = False
verbs = []
for line in f:
	if line.startswith(u"===Verbi==="):
		seen_verb = True
	elif "{{" in line or ":" in line:
		pass
	elif seen_verb and line.startswith(u"#") and "{{" not in line:
		verb = line.replace("#", "").replace("[", "").replace("]","").replace("\n","")
		verb = verb.strip()
		if "<" in verb:
			verb = verb.split("<")[0]
		if "," not in verb:
			if " " in verb:
				verb = verb.split(" ")[0]
			verbs.append(verb)
		else:
			verbs.extend(verb.split(","))
		seen_verb = False

verbs = list(set(verbs))
random.shuffle(verbs)
fo = codecs.open("verbs.txt", "w", encoding="utf-8")
for verb in verbs:
	fo.write(verb.strip() + "\n")
fo.close()
