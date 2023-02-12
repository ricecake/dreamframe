#! /usr/bin/env python
import sys, random, argparse
##Biman Gujral
class New_Class(object):
    pass
def sentence_generator(rules, symbol, non_terminal, sentence, sentence_tree,sentence_bracket, indent):
    rand_count={}           #stores rule as value, key is the cumulative probability of the rule
    #for writing tree structure
    if len(sentence_tree)>1 and sentence_tree[len(sentence_tree)-1]==")":
            sentence_tree.append("\n"+indent)
    elif len(sentence_tree)>1 and sentence_tree[len(sentence_tree)-1][3:] not in non_terminal.keys():
            sentence_tree.append("\n"+indent)
    #base case
    if symbol not in non_terminal.keys():
        sentence.append(symbol)
        sentence_bracket.append(symbol)
        sentence_tree.append("  "+symbol)
    else:
        bracket_flag=0
        if symbol=="S" or symbol=="S_QUES":
            sentence_bracket.append("{")
        if ("NP" in symbol or "Pronoun" in symbol) and sentence_bracket[len(sentence_bracket)-1]!="[":
            sentence_bracket.append("[")
            bracket_flag=1
        sentence_tree.append("  "+"("+symbol)
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
            sentence_generator(rules,s,non_terminal,sentence, sentence_tree,sentence_bracket,indent+"   "+len(apply_rule[1])*" ")  #extra space for bracket
        if symbol=="S" or symbol=="S_QUES":
            sentence_bracket.append("}")
        if ("NP" in symbol or "Pronoun" in symbol) and bracket_flag==1:
            sentence_bracket.append("]")
        sentence_tree.append(")")
def main(argv):
    parser = argparse.ArgumentParser(description='Options and Arguments')
    parser.add_argument('-t', action='store_true', help="Print parse tree to show the underlying sentence structure")
    parser.add_argument('-b', action='store_true', help="Print brackets to show partial sentence structure")
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
    sentence_tree_list=[]
    sentence_bracket_list=[]
    for i in range(0,c.num_sent):
        sentence = []
        sentence_tree=[]
        sentence_bracket=[]
        sentence_generator(rules,'ROOT',non_terminal, sentence,sentence_tree,sentence_bracket,"")
        sentence_list.append(' '.join(sentence))
        sentence_tree_list.append(''.join(sentence_tree))
        sentence_bracket_list.append(' '.join(sentence_bracket))
    for sen in sentence_list:
        print(sen)
    if(c.t):
        for each in sentence_tree_list:
            print(each)
    if(c.b):
        for each in sentence_bracket_list:
            print(each)

if __name__ == "__main__":
    main(sys.argv[1:])

