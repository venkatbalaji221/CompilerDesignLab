from itertools import takewhile
import string
import pandas as pd
import argparse
epsil = '\u03b5'
terminals = []
nonterminals = []
ssymb = ""
freq = 0

def get_id(id_dict, id_value):   # returns terminal name for given token id
    for key, value in id_dict.items():
        if value == id_value:
            return key

def parse(userip, ssymb, ptable): # parses user input using parse table
    flag = 0
    stack = ["$", ssymb]
    ip_index = 0
    while stack[len(stack)-1] != '$':
        print("")
        top = stack[len(stack) - 1]
        print("stack: ", stack)

        # current input
        currentip = userip[ip_index]
        print("Input: ", userip[ip_index:])


        # if top in terminals and term_id[top] == token_id[currentip]:
        #     stack.pop()
        #     print("MATCHED: "+str(top)+" == "+str(currentip))
        #     ip_index = ip_index + 1

        if top in terminals:
            if term_id[top] == token_id[currentip]:  # checking equality of terminals
                stack.pop()
                print("MATCHED: " + str(top) + " == " + str(currentip))
                ip_index = ip_index + 1
            else:
                flag = 1
                print("Terminals not matched on stacks")
                break

        else:
            # finding value for key in table
            if currentip != "$":
                ip_id = get_id(term_id, token_id[currentip])
                key = top, ip_id
                print("lookup: "+str(key))
            else:
                key = top, '$'
                print("lookup: "+str(key))

            # top of stack terminal => not accepted
            if key not in ptable:
                flag = 1
                print("No entry in the parse table!")
                break

            value = ptable[key]
            print("prod: "+str(top)+" -> "+str(value))
            if value != [epsil]:
                value = value[::-1]
                stack.pop()
                for element in value:       # pusing productin symbols in reverse order
                    stack.append(element)
            else:
                stack.pop()


    if flag == 0:
        print("\nstack: "+str(stack))
        print("Input: "+str(userip[ip_index:]))
        print("Input syntactically correct!\n")
    else:
        print("\nstack: " + str(stack))
        print("Input: " + str(userip[ip_index:]))
        print("Input syntactically Wrong!\n")


def ll1():       # parse table generator
    table = {}
    for lhs in productions:
        for st in productions[lhs]:
            first_set = set()
            for j in range(0, len(st)):
                if st[j] == epsil:
                    c = [epsil]
                else:
                    c = first_dict[st[j]]
                if epsil not in c:
                    first_set = first_set.union(c)
                    break
                first_set = first_set.union(c)

            for a in first_set:                 # Adding entry for all symbols in first(lhs)
                if a == epsil:
                    continue
                if (lhs, a) in table.keys():
                    c = table[lhs, a]
                    c.append(st)
                    table[lhs, a] = c
                else:
                    table[lhs, a] = st

            if epsil in first_set:             # If epsilon in first(rhs) add entry for all symbols in follow(lhs)
                for b in follow_dict[lhs]:
                    table[lhs, b] = st

    # for key, val in table.items():
    #     print(key, "=>", val)
    new_table = {}                          # Manipulation for representing as a dataframe using pandas
    for pair in table:
        new_table[pair[1]] = {}
    for pair in table:
        new_table[pair[1]][pair[0]] = table[pair]

    print("\n")
    print("\nParsing Table in matrix form\n")
    print(pd.DataFrame(new_table).fillna('-'))
    print("\n")
    return table


def follow_first(s, productions):          # First part of calculating follow sets algo
    sub_set = set()
    for st in productions[s]:
        for i in range(0, len(st)):
            if st[i] in nonterminals:
                for j in range(i+1, len(st)):
                    c = first_dict[st[j]]
                    sub_set = sub_set.union(c)-{epsil}
                    if epsil not in c:
                        break
                follow_dict[st[i]] = follow_dict[st[i]].union(sub_set)
                sub_set.clear()


def follow(s, productions):              # second part of calculating follow sets algo
    flag = 0
    for st in productions[s]:
        for i in range(0, len(st)-1):
            if st[i] in nonterminals:
                for j in range(i+1, len(st)):
                    d = first_dict[st[j]]
                    if epsil in d and j == len(st)-1:  # first(c) in aBc has epsil
                        flag = 1
                    if epsil not in d:
                        break
                if flag == 1:
                    c = follow_dict[s]
                    follow_dict[st[i]] = follow_dict[st[i]].union(c)
        if st[len(st)-1] in nonterminals:
            c = follow_dict[s]
            follow_dict[st[len(st)-1]] = follow_dict[st[len(st)-1]].union(c)


def first(s, productions):               # calculates first set
    ans = []
    if s in nonterminals:
        for st in productions[s]:
            if st[0] in terminals:                    # If terminal in production stop and move to next production
                ans.append(st[0])
                continue
            elif st[0] in nonterminals:               # If non-terminal, iterate over symbols until anyone doesn't derive epsilon in first set
                j = 0
                sub_first = first(st[j], productions)
                for i in sub_first:
                    if i != epsil:
                        ans.append(i)
                j += 1
                while epsil in sub_first and j < len(st):
                    sub_first = first(st[j], productions)
                    j += 1
                    for i in sub_first:
                        if i != epsil:
                            ans.append(i)
                if j == len(st) and epsil in sub_first:
                    ans.append(epsil)
            elif st[0] == epsil:               # If production is epsilon, add epsilon
                ans.append(epsil)
    else:
        ans.append(s)
        # print(ans)
    return set(ans)

def left_recursion():
    perfect = {}  # Dictionary having productions not starting with same non-terminal

    def calcPerfect():  # Calculates perfect when grammar is updated
        for head, tail in productions.items():
            temp = []
            for sym in tail:
                if sym[0] != head:
                    temp.append(sym)
            perfect[head] = temp

    calcPerfect()

    def eliminate(k):  # Function for eliminating left recursion
        tempElim = []  # List for updated current production
        tempDash = []  # List for new dash production
        flag = 0
        valve = 0
        for prodElim in productions[nonterminals[k]]:
            if prodElim[0] == nonterminals[k]:  # If Left Recursion
                flag = 1
                break
        if flag == 1:
            for sym in perfect[nonterminals[k]]:
                # tempElim.append(str(sym+serial[k]+"'"))
                sym.append(str(nonterminals[k] + "'"))
                tempElim.append(sym)

            for prodElim in productions[nonterminals[k]]:
                if prodElim[0] == nonterminals[k]:
                    data = prodElim[1:]
                    data.append(str(nonterminals[k] + "'"))
                    nonterminals.append(str(nonterminals[k] + "'"))
                    tempDash.append(data)

            tempDash.append(["\u03B5"])  # Epsilon Production
            # If recursion encountered, update current production and insert dash production
            productions[nonterminals[k]] = tempElim
            productions[str(nonterminals[k] + "'")] = tempDash
            calcPerfect()

    for i in range(len(nonterminals)):  # Main Loop for removing indirect left recursion
        prod = productions[nonterminals[i]]
        dump = []
        for j in range(0, i):
            for form in prod:
                if form[0] == nonterminals[j]:
                    temp = form[1:]
                    dump.append(form)
                    for sym in productions[nonterminals[j]]:
                        prod.append(sym + temp)

            for form in dump:  # dump is to store strings that are to be removed from the production list
                if form in prod:
                    prod.remove(form)

        productions[nonterminals[i]] = prod
        calcPerfect()
        eliminate(i)

def left_factor(head, prod):
    global freq

    def group_by(ls):  # Finds set of string starting with same symbol
        d = {}
        ls = [y[0] for y in rules]
        y = max(ls, key=ls.count)
        if ls.count(y) == 1:
            return d
        for i in rules:
            if i[0] == y:
                if y not in d:
                    d[y] = []
                d[y].append(i)
        # print(d)
        return d

    def prefix(x):  # Function to find longest prefix
        global freq
        occ = max(x, key=x.count)
        if freq == 0:
            freq = x.count(occ)
            return True
        elif freq == x.count(occ):
            return True
        else:
            return False

    rules = prod
    common = []
    starting = head
    # print("rules:" + str(head) + "->" + str(rules))

    while True:
        # Finding longest prefix
        common.clear()
        for k, l in group_by(rules).items():
            # print(str(list(zip(*l))))
            r = [l[0] for l in takewhile(prefix, zip(*l))]  # sends lists of 1st,2nd and so on letters of considered strings to prefix
            # print(r)
            common = r       # list of common prefix symbols

        if len(common) == 0:  # If no more left factoring, break the loop
            break

        far = len(common)
        # Evaluating next new production
        index = []  # list storing strings starting with prefix
        for k in rules:
            if k[0:far] == common:
                index.append(k)

        # print(index)
        new_alphabet = alphabets.pop()  # Taking new symbol
        nonterminals.append(new_alphabet)
        data = []
        c = [i for i in common]
        c.append(new_alphabet)
        data.append(c)
        # print(data)

        for j in rules[:-1]:
            if j not in index:
                data.append(j)
        if rules[-1] not in index:
            data.append(rules[-1])


        data1 = [i for i in data]    # data1 is modified current production
        factor_dict[starting] = data1

        # New production
        data.clear()
        new_prod = ""
        new_prod += new_alphabet + "->"
        # print(index)
        for j in index[0:]:
            if j == common:
                data.append([epsil])
            else:
                data.append(j[len(common):])
            # print(data)
        factor_dict[new_alphabet] = data    # data is generated new production being stored in seperate dictionary
        # print(data)                       # Current dictionary being iterated not to be modified in the loop
        rules = data
        freq = 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-g', "--grammar", help="Enter the file name with path", required=True)
    args = vars(ap.parse_args())
    grammarfile = args["grammar"]
    grammar = open(grammarfile, "r")

    productions = dict()
    first_dict = dict()
    follow_dict = dict()
    factor_dict = dict()
    term_id = dict()

    for line in grammar:
        l = line.strip().split(" -> ")
        if l[0][0] == '1':
            nonterminals = str(l[0][2:]).split(' ')
            n = len(nonterminals)
        elif l[0][0] == '2':
            term_pair = str(l[0][2:]).split(' ')
            for i in range(len(term_pair)):
                temp = term_pair[i].split('|')
                term_id[temp[0]] = temp[1]
                terminals.append(temp[0])
        elif l[0][0] == '3':
            ssymb = l[0][2]
        else:
            lhs = l[0]
            rhs = [a.split(" ") for a in l[1].split(" | ")]
            for i in range(len(rhs)):
                if rhs[i] == ['eps']:
                    rhs[i][0:] = [epsil]
            productions[lhs] = rhs

                                                    # INPUT Grammar
    print("\n             Given Grammar")
    for lhs in productions:
        print(str(lhs) + " -> ", end="")
        for i in range(len(productions[lhs]) - 1):
            print(' '.join(productions[lhs][i]), end="")
            print(" | ", end="")
        print(' '.join(productions[lhs][-1]))

                                                    # LEFT RECURSION calculation

    left_recursion()
    print('\n      Left Recursion removed\n')
    for lhs in productions:
        print(str(lhs) + " -> ", end="")
        for i in range(len(productions[lhs])-1):
            print(' '.join(productions[lhs][i]), end="")
            print(" | ", end="")
        print(' '.join(productions[lhs][-1]))

                                                         # LEFT FACTORING

    alphabets = list(string.ascii_uppercase)
    alphabets = list(set(alphabets) - set(terminals) - set(nonterminals))  # symbols used for new productions

    for lhs in productions:
        left_factor(lhs, productions[lhs])
    for lhs in factor_dict:                  # productions stored in factor_dict appended to main dict
        productions[lhs] = factor_dict[lhs]

    print('\n        Left Factored\n')
    for lhs in productions:
        print(str(lhs) + " -> ", end="")
        for i in range(len(productions[lhs]) - 1):
            print(' '.join(productions[lhs][i]), end="")
            print(" | ", end="")
        print(' '.join(productions[lhs][-1]))


    # nonterminals = list(set(nonterminals))

                                                 # FIRST SET calculation

    print('\n          First sets\n')
    for sym in terminals:                       # first of terminal is itself
        first_dict[sym] = first(sym, productions)
    for lhs in productions:
        first_dict[lhs] = first(lhs, productions)
        print(str(lhs)+" => ", end="")
        print(' '.join(first_dict[lhs]))

                                                #FOLLOW SET calculation

    print('\n             Follow sets\n')

    for lhs in productions:
        follow_dict[lhs] = set()

    follow_dict[ssymb] = follow_dict[ssymb].union('$')       # dollar in follow of start symbol
    store_dict = dict()

    while store_dict != follow_dict:                        # operations are done until follow_dict is not modified
        for head, tail in follow_dict.items():
            store_dict[head] = tail
        for lhs in productions:
            follow_first(lhs, productions)
        for lhs in productions:
            follow(lhs, productions)

    for lhs in productions:
        print(str(lhs) + " => ", end="")
        print(' '.join(follow_dict[lhs]))

    table = ll1()

    f = open("tokens.txt", "r+")            # reading tokens generated by lex tool
    token_input = []
    token_id = {}
    for line in f.readlines():
        temp = line.strip().split(' ')
        token_id[temp[1]] = temp[0]
        token_input.append(temp[1])
    token_input.append("$")                 # Appending $ at the last of user input


    parse(token_input, ssymb, table)        # calling parser

