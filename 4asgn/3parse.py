import string
nterm = ["E", "E'", "T", "T'", "F"]
gram = {'E': [['T', "E'"]], "E'": [["+", "T", "E'"], ["\u03b5"]], 'T': [["F", "T'"]], "T'": [["*", "F", "T'"], ["\u03b5"]], 'F': [["(", "E", ")"], ["id"]]}
point = 0  # pointer
pmem = 0
error = 0   # when input is insufficient
serial = nterm
call = {0: "E()", 1: "Eprime()", 2: "T()", 3: "Tprime()", 4: "F()"}  # function calling
f = open("parse.txt", 'r')
word = f.readline().strip('\n')

def identify(pointer):   # For reading identifier
    global word
    count = 0
    if word[pointer].islower():
        count += 1
        pointer += 1
        while word[pointer].isdigit() or word[pointer].islower():
            pointer += 1
            count += 1
            if pointer == len(word):
                break
        return count, True
    else:
        return count, False

def F():
    global serial, call, point, word, error
    flag = 0
    pmem = point
    pinit = point
    print(point)
    for prod in gram["F"]:
        if prod[0] == 'id':
            width, status = identify(point)
            if status:
                print(word[point:point+width] + " matched")
                if flag == 0:
                    pmem = point
                    point += width
                    flag = 1
                return
            else:
                if width > 0:
                    print("Invalid Identifier: " + word[point:point + width])
                if flag == 1:
                    point = pmem
                    flag = 0
        else:
            for sym in prod:
                if sym in nterm:
                    num = serial.index(sym)
                    print(call[num])
                    eval(call[num])
                elif word[point] == sym:
                    if flag == 0:
                        pmem = point
                        flag = 1
                    print(word[point]+" matched")
                    point += 1
                else:
                    if flag == 1:
                        point = pmem
                        flag = 0
                        print("backtrack")
                    break
            if sym == prod[-1]:
                return

    if pinit == point:   # If input is not matched to any F production, backtrack recursively
        error = 1
    return


def Tprime():
    global serial, call, point, word, error
    flag = 0
    pmem = point
    # print(point)
    for prod in gram["T'"]:
        for sym in prod:
            if sym == '\u03b5':
                print(sym)
                return
            if sym in nterm:
                num = serial.index(sym)
                print(call[num])
                eval(call[num])
            elif point < len(word):
                if word[point] == sym:
                    if flag == 0:
                        pmem = point
                        flag = 1
                    print(word[point]+" matched")
                    point += 1
            else:
                if flag == 1:
                    point = pmem
                    flag = 0
                    print("backtrack")
                break
            if error == 1:
                if flag == 1:
                    point = pmem
                    flag = 0
                error = 0
                print("backtrack")
                break
    return

def T():
    global serial, call, point, word
    flag = 0
    pmem = point
    # print(point)
    for prod in gram["T"]:
        for sym in prod:
            if sym in nterm:
                num = serial.index(sym)
                print(call[num])
                eval(call[num])
            elif word[point] == sym:
                if flag == 0:
                    pmem = point
                    flag = 1
                print(word[point]+" matched")
                point += 1

            else:
                if flag == 1:
                    point = pmem
                    flag = 0
                    print("backtrack")
                break
    return


def Eprime():
    global serial, call, point, word, error
    flag = 0
    pmem = point
    # print(point)
    for prod in gram["E'"]:
        for sym in prod:
            if sym == '\u03b5':
                print(sym)
                return
            if sym in nterm:
                num = serial.index(sym)
                print(call[num])
                eval(call[num])
            elif word[point] == sym:
                if flag == 0:
                    pmem = point
                    flag = 1
                print(word[point]+" matched")
                point += 1
            else:
                if flag == 1:
                    point = pmem
                    flag = 0
                    print("backtrack")
                break
            if error == 1:
                if flag == 1:
                    point = pmem
                    flag = 0
                error = 0
                print("backtrack")
                break
    return

def E():
    global serial, call, point, word
    flag = 0
    pmem = point

    for prod in gram['E']:
        for sym in prod:
            if sym in nterm:
                num = serial.index(sym)
                print(call[num])
                eval(call[num])
            elif word[point] == sym:
                if flag == 0:
                    pmem = point
                    flag = 1
                print(word[point]+" matched")
                point += 1
            else:
                if flag == 1:
                    point = pmem
                    flag = 0
                    print("backtrack")
                break
    print(point)
    if word[point] == '$':
        print('Success')
    else:
        print('Failure')

E()







