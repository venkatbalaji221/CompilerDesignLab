from itertools import takewhile
import string
freq = 0

def group_by(ls):    # Finds set of string starting with same symbol
    d = {}
    ls = [y[0] for y in rules]
    y = max(ls, key=ls.count)
    if ls.count(y) == 1:
        return d
    for i in rules:
        if i.startswith(y):
            if y not in d:
                d[y] = []
            d[y].append(i)
    # print(d)
    return d

def prefix(x):       # Function to find longest prefix
    global freq
    occ = max(x, key=x.count)
    if freq == 0:
        freq = x.count(occ)
        return True
    elif freq == x.count(occ):
        return True
    else:
        return False
    # return len(x) - len(set(x)) > 0
    # return len(set(x)) == 1


rules = []
common = []
alphabets = list(string.ascii_uppercase)   # symbols used for new productions

# s = "S->iEtS|iEtSeS|a"
# s = "A->aAB| aABC | aAc|d"
# s = "S->  bSSaaS| bSSaSb |bSb|a  "
s = "S-> aSSbS | aSaSb | abb | b"


print("Initial Grammar: "+s)
print("\nResult:")

while True:
    s = ''.join(s.split())    # Remove spaces
    split = s.split("->")
    rules.clear()
    starting = split[0]
    for i in split[1].split("|"):
        rules.append(i)
    # print("rules:"+str(rules))

# Finding longest prefix
    common.clear()
    for k, l in group_by(rules).items():
        # print(str(list(zip(*l))))
        r = [l[0] for l in takewhile(prefix, zip(*l))]    # sends lists of 1st,2nd and so on letters of considered strings to prefix
        print(r)
        common.append(''.join(r))
    # print("commmon"+str(common))

    if len(common) == 0 or common[0] == "\u03B5":     # If no more left factoring, break the loop
        print(s)
        break

# Evaluating next new production
    for i in common:
        # print(common)
        index = []                # list storing strings starting with prefix
        for k in rules:
            if k.startswith(i):
                index.append(k)
        # print(index)

        new_alphabet = alphabets.pop()            # Taking new symbol
        print(starting+"->"+i+new_alphabet, end="")

        for j in rules[:-1]:
            if j not in index:
                print("|"+j, end="")
        if rules[-1] not in index:
            print("|"+rules[-1])
        else:
            print("")

        # New production
        new_prod = ""
        new_prod += new_alphabet+"->"

        for j in index[:-1]:
            stringtoprint=j.replace(i, "", 1)+"|"
            if stringtoprint == "|":
                new_prod += "\u03B5" + "|"
            else:
                new_prod += j.replace(i, "",  1)+"|"

        stringtoprint = index[-1].replace(i, "", 1)+"|"
        if stringtoprint == "|":
            new_prod += "\u03B5"
        else:
            new_prod += index[-1].replace(i, "", 1)
        s = new_prod
        freq = 0

