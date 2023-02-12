#! /usr/bin/env python
import sys, random, argparse
##Biman Gujral
class New_Class(object):
    pass
def sentence_generator(rules, symbol, non_terminal, sentence):
    rand_count={}           #stores rule as value, key is the cumulative probability of the rule
    #for writing tree structure
    #base case
    if symbol not in non_terminal.keys():
        sentence.append(symbol)
    else:
        total_count = float(non_terminal[symbol])
        current_count=0
        #find all rules applicable for given non-terminal symbol
        for rule in rules:
            if rule[1]==symbol:
                current_count = current_count + float(rule[0])/total_count
                rand_count[current_count] = rule
        r = random.random()
        apply_rule = []
        #select rule according to the number generated and probabilities calculated
        for prob in sorted(rand_count.keys()):
            if prob >= r:
                apply_rule = rand_count[prob]
                break
        for s in apply_rule[2:len(apply_rule)]:
            sentence_generator(rules,s,non_terminal,sentence)  #extra space for bracket
def main(argv):
    parser = argparse.ArgumentParser(description='Options and Arguments')
    parser.add_argument('g_arg', help="Path of the grammar file to be used")
    parser.add_argument('num_sent', nargs='?',default=1, type=int, help="Number of sentences to be generated (Default: 1)")
    c = New_Class()
    parser.parse_args(args=argv, namespace=c)
    grammar = open(c.g_arg)

    lines = grammar.readlines()
    rules=[]
    non_terminal={} #stores total of odds of non-terminal symbol which is the key
    for l in lines:
        if l!='\n' and l[0]!='#':
            l_tokens = l.split()
            for token in l_tokens:
                #ignore comments in grammar
                if '#' in token:
                    l_tokens=l_tokens[0:l_tokens.index(token)]
                    break
            rules.append(l_tokens)
            #calculate cumulative probabilities
            if l_tokens[1] not in non_terminal.keys():
                non_terminal[l_tokens[1]] = float(l_tokens[0])
            else:
                non_terminal[l_tokens[1]] += float(l_tokens[0])
    sentence_list=[]
    for i in range(0,c.num_sent):
        sentence = []
        sentence_generator(rules,'ROOT',non_terminal, sentence)
        sentence_list.append(' '.join(sentence))
    for sen in sentence_list:
        print(sen)

if __name__ == "__main__":
    main(sys.argv[1:])

