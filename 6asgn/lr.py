class state:

    def __init__(self):
        self.red_flag = 0
        self.dot_dict = dict()
        self.items_dict = dict()
        self.la_dict = dict()
    pass

def first_set(s, productions):               # calculates first set
    ans = []
    if s in nonterminals:
        for st in productions[s]:
            if st[0] in terminals:                    # If terminal in production stop and move to next production
                ans.append(st[0])
                continue
            elif st[0] in nonterminals:               # If non-terminal, iterate over symbols until anyone doesn't derive epsilon in first set
                j = 0
                sub_first = first_set(st[j], productions)
                for i in sub_first:
                    if i != epsil:
                        ans.append(i)
                j += 1
                while epsil in sub_first and j < len(st):
                    sub_first = first_set(st[j], productions)
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

def print_state(st):
    print("\tItems\t")
    print(st.items_dict)
    print("\tDotlist\t")
    print(st.dot_dict)
    print("\tLA list\t")
    print(st.la_dict)
    print("reduce flag:" + str(st.red_flag) )
if __name__ == "__main__":
    grammar = open("grammar.txt", 'r')

    state_num = 0
    nonterminals = []
    terminals = []
    first_dict = dict()
    term_id = dict()
    productions = dict()
    epsil = '\u03b5'

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

    print("\n             Given Grammar")
    for lhs in productions:
        print(str(lhs) + " -> ", end="")
        for i in range(len(productions[lhs]) - 1):
            print(' '.join(productions[lhs][i]), end="")
            print(" | ", end="")
        print(' '.join(productions[lhs][-1]))


    print('\n          First sets\n')
    for sym in terminals:  # first of terminal is itself
        first_dict[sym] = first_set(sym, productions)
    for lhs in productions:
        first_dict[lhs] = first_set(lhs, productions)
        print(str(lhs) + " => ", end="")
        print(' '.join(first_dict[lhs]))

    stlist = []
    # Initial state0
    a = state()
    a.items_dict["S'"] = ['.', 'S']
    a.la_dict["S'"] = ['$']
    a.dot_dict['S'] = [["S'", '.', 'S'], ['$']]

    # print_state(a)
    



