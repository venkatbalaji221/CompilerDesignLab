import string
value = 1
while 1:
    if value == '0':
        break
    exp = input("\nInput Expression: ")

    # p-pointer
    p = 0
    flag = 0
    operators = ["<", ">", "<=", ">=", "=", "<>"]
    alphabet = list(string.ascii_letters)
    identifier = ""

    # checks operator
    def checkop(j):
        if exp[j:j+2] == "<=":
            print("(relop, LT)")
            return j+2
        if exp[j:j+2] == "<>":
            print("(relop, NE)")
            return j+2
        if exp[j:j+2] == ">=":
            print("(relop, GE)")
            return j+2
        if exp[j] == ">":
            print("(relop, GT)")
            return j+1
        if exp[j] == "<":
            print("(relop, LT)")
            return j+1
        if exp[j] == "=":
            print("(relop, EQ)")
            return j+1

    # checks identifier
    def checkid (j):
        global flag, identifier
        identifier = exp[j]
        j += 1
        while j < len(exp):
            if exp[j] in alphabet or exp[j].isdigit() or exp[j] == "_":
                identifier += exp[j]
                j += 1
            else:
                if exp[j] == " ":
                    j += 1
                if exp[j] in operators:
                    print("(id, " + identifier + ")")   # END of identifier token
                    return j
                else:
                    # Invalid character
                    flag = 1
                    return j

        if j == len(exp):
            print("(id, " + identifier + ")")
            return j

    def checkdigits(numb, j):  # Iterates till digits are encountered
        global flag
        while exp[j].isdigit():
            numb += exp[j]
            j += 1
            if j == len(exp):
                break
        if j != len(exp):
            if exp[j] != "." and exp[j] != " " and exp[j] != "E" and exp[j] not in operators:
                flag = 1
        return numb, j

    def checknum(j):
        global flag
        num = exp[j]
        j += 1
        if j == len(exp):
            return num, j   # single digit

        num, j = checkdigits(num, j)
        if flag == 1 or j == len(exp) or exp[j] == " " or exp[j] in operators:  # End ot Token or Invalid Token
            return num, j

        # checking decimal
        if exp[j] == ".":
            num += exp[j]
            j += 1
            if j == len(exp) or exp[j] == " " or exp[j] in operators:
                flag = 1  # Invalid number with no decimals
                return num, j

            num, j = checkdigits(num, j)
            if flag == 1 or j == len(exp) or exp[j] == " " or exp[j] in operators:
                return num, j

        # checking Exponent
        if exp[j] == "E":
            num += exp[j]
            j += 1
            if j == len(exp) or exp[j] == " " or exp[j] in operators:
                flag = 1   # Invalid Exponent
                return num, j
            if exp[j] in ["+", "-"]:
                num += exp[j]
                j += 1
                if j == len(exp) or exp[j] == " " or exp[j] in operators:
                    flag = 1   # Invalid Exponent
                    return num, j

            num, j = checkdigits(num, j)
            if flag == 1 or j == len(exp) or exp[j] == " " or exp[j] in operators:
                return num, j


    print("\nToken List produced:\n")

    while p < len(exp):   # Main code

        if exp[p] == " ":
            p += 1
        # checking if token
        elif exp[p] == "i" and p+1 < len(exp):
            if exp[p:p+2] == "if" and exp[p+2] == " ":
                print("(if, if)")
                p = p+2
            else:
                p = checkid(p)
                if flag == 1:
                    flag = 0
                    print("Invalid Character found!(" + exp[p] + ")")
                    while exp[p] != " ":
                        p += 1
                        if p == len(exp):
                            break

        # checking else token
        elif exp[p] == "e" and p+3 < len(exp):
            if exp[p:p+4] == "else" and exp[p+4] == " ":
                print("(else, else)")
                p = p+4
            else:
                p = checkid(p)
                if flag == 1:
                    flag = 0
                    print("Invalid Character found!(" + exp[p] + ")")
                    while exp[p] != " ":
                        p += 1
                        if p == len(exp):
                            break
        # checking then token
        elif exp[p] == "t" and p+3 < len(exp):
            if exp[p:p+4] == "then" and exp[p+4] == " ":
                print("(then, then)")
                p = p+4
            else:
                p = checkid(p)
                if flag == 1:
                    flag = 0
                    print("Invalid Character found!(" + exp[p] + ")")
                    while exp[p] != " ":
                        p += 1
                        if p == len(exp):
                            break
        # chekcing number
        elif exp[p].isdigit():
            word = ""
            number, p = checknum(p)
            if flag == 1:
                flag = 0
                while exp[p] != " ":
                    word += exp[p]
                    p += 1
                    if p == len(exp):
                        break
                print("Invalid number!(" + number + word + ")")
            else:
                print("(number, " + number + ")")

        # checking reop
        elif exp[p] in operators:
            p = checkop(p)
        # checking identifier
        elif exp[p] in alphabet:
            p = checkid(p)
            if flag == 1:
                flag = 0
                print("Invalid Character found!(" + exp[p] + ")")
                while exp[p] != " ":
                    p += 1
                    if p == len(exp):
                        break
    value = input("\ncontinue(1) Exit(0): ")






