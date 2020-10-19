f = open("recursion.txt", 'r+')  # Reads grammar from file
gram = {}                   # Grammar dictionary
serial = []                 # List storing serial numbers for non terminals
perfect = {}                # Dictionary having productions not starting with same non-terminal
n = 0                       # No of Non-Terminals
for line in f.readlines():
    temp = list(line.strip('\n').split('->'))
    gram[temp[0]] = list(temp[1].split('|'))
    serial.append(temp[0])
    n += 1

# print(grammar)

def calcPerfect():            # Calculates perfect when grammar is updated
    global gram, perfect
    for head, tail in gram.items():
        temp = []
        for sym in tail:
            if sym[0] != head:
                temp.append(sym)
        perfect[head] = temp

calcPerfect()

def eliminate(k):            # Function for eliminating left recursion
    tempElim = []            # List for updated current production
    tempDash = []            # List for new dash production
    flag = 0
    for prodElim in gram[serial[k]]:
        if prodElim[0] == serial[k]:  # If Left Recursion
            flag = 1
            for sym in perfect[serial[k]]:
                tempElim.append(str(sym+serial[k]+"'"))
            tempDash.append(str(prodElim[1:] + serial[k] + "'"))
    tempElim = list(set(tempElim))

    tempDash.append("\u03B5")               # Epsilon Production
    if flag == 1:                         # If recursion encountered, update current production and insert dash production
        gram[serial[k]] = tempElim
        gram[str(serial[k] + "'")] = tempDash
    calcPerfect()


for i in range(0, n):           # Main Loop for removing indirect left recursion
    prod = gram[serial[i]]
    dump = []
    for j in range(0, i):
        for form in prod:
            if form[0] == serial[j]:
                temp = form[1:]
                dump.append(form)
                for sym in gram[serial[j]]:
                    prod.append(sym+temp)
        for form in dump:                      # dump is to store strings that are to be removed from the production list
            if form in prod:
                prod.remove(form)

    gram[serial[i]] = prod
    calcPerfect()
    eliminate(i)

for prod, exp in gram.items():
    print(prod+"->"+str(exp))


# sample inputs
# E:E+T||T||F
# T:T*F||F
# F:(E)||id||E||T

# X:XSb||Sa||b
# S:Sb||Xa||a

# S:(L)||a
# L:L,S||S





