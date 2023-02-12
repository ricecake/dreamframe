from nltk.parse.generate import generate, demo_grammar
from nltk import PCFG
grammar = PCFG.fromstring("""
PRO -> S ',' MODS [.75] | S [.25]
MODS -> N [.75] | N ',' MODS [.25]
S -> NP VP [1]
PP -> P NP [1]
NP -> Det N [1]
VP -> V NP [1]
Det -> 'a' [.9] | 'the' [.1]
N -> 'dog' [.5] | 'cat' [.5]
V -> 'chased' [.5] | 'sat' [.5]
P -> 'on' [.5] | 'in' [.5]
""")
print(grammar)

for sentence in generate(grammar, n=30):
    print(' '.join(sentence))


# PRO -> S
# PRO -> S ',' MODS
# MODS -> N
# MODS -> N ',' MODS
# S -> NP VP
# PP -> P NP
# NP -> Det N | NP PP
# VP -> V NP | VP PP
# Det -> 'a' | 'the'
# N -> 'dog' | 'cat'
# V -> 'chased' | 'sat'
# P -> 'on' | 'in'
