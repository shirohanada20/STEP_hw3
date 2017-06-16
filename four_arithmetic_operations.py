# coding: utf-8

#数字の文字列を受け取ったらint型に直してその数の数字型tokenを返す
def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index): #+を受け取ったらPLUS型のtokenを返す
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index): #-を受け取ったらMINUS型のtokenを返す
    token = {'type': 'MINUS'}
    return token, index + 1

def readMultiply(line, index): #*を受け取ったらMULTIPLY型のtokenを返す
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def readDivide(line, index): #/を受け取ったらDIVIDE型のtokenを返す
    token = {'type': 'DIVIDE'}
    return token, index + 1


def readOpenparen(line, index): #(を受け取ったらOPENPAREN型のtokenを返す
    token = {'type': 'OPENPAREN'}
    return token, index + 1


def readCloseparen(line, index): #)を受け取ったらCLOSEPAREN型のtokenを返す
    token = {'type': 'CLOSEPAREN'}
    return token, index + 1

#文字列を受け取ったら文字の分類を含むtokenの集合を返す(構文解析)。
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiply(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readOpenparen(line, index)
        elif line[index] == ')':
            (token, index) = readCloseparen(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens

#加減記号のみを含む式(tokens)、評価範囲を示す２つの数字を受け取ったら加減について計算を行い式の値を返す。
def evaluateplusminus(tokens, startpos, endpos):
    answer = 0
    tokens.insert(startpos-1, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = startpos
    while index < endpos+1:
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax'
        index += 1
    return answer

#乗除を含む式(tokens)、評価範囲を示す２つの数字を受け取ったら乗除のみを計算した式(tokens)を返す。
def evaluatemultidiv(tokens, startpos, endpos):
    index = startpos
    while index < endpos:
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLY':
                tokens[index - 2]['number'] *= tokens[index]['number']
                tokens.pop(index -1)
                tokens.pop(index -1)
                index -= 1
                endpos -= 2
            elif tokens[index - 1]['type'] == 'DIVIDE':
                tokens[index - 2]['number'] /= 1.0*(tokens[index]['number'])
                tokens.pop(index - 1)
                tokens.pop(index - 1)
                index -= 1
                endpos -=2
        index += 1
    return tokens

#括弧を含む式(tokens)を受け取ったら括弧内の値を計算し括弧を除いた式(tokens)を返す。
def evaluateParenthesis(tokens, pos):
    evaltokens = tokens
    index = pos
    openpos = 0
    closepos = 0
    while index < len(evaltokens):
        if evaltokens[index]['type'] == 'OPENPAREN':
            openpos = index
            index += 1
            while evaltokens[index]['type'] != 'CLOSEPAREN':
                if evaltokens[index]['type'] == 'OPENPAREN':
                    evaltokens = evaluateParenthesis(evaltokens, index)
                index += 1
            if evaltokens[index]['type'] == 'CLOSEPAREN':
                protokens = evaluatemultidiv(evaltokens, openpos+1, index)
                index = openpos
                while protokens[index]['type'] != 'CLOSEPAREN':
                    index += 1
                answer = evaluateplusminus(protokens, openpos+2, index)
                removerange = openpos
                while removerange < index + 2:
                    protokens.pop(openpos)
                    removerange += 1
                protokens.insert(openpos, {'type': 'NUMBER', 'number': answer})
                index = openpos
                evaltokens = protokens
        index += 1
    return evaltokens

#tokensを受け取って式の値を返す。括弧内の式→乗除→加減の順序で評価する。
def evaluate(tokens):
    answer = evaluateplusminus(evaluatemultidiv(evaluateParenthesis(tokens, 0), 1, len(tokens)), 1, len(tokens))
    return answer

def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("10/2/5*3", 3)
    #order : realnumber, real and decimal, decimal
    #order : number only, plus, minus, multiply, divide, plus and minus, multiply and divide, plus and multiply or divide

    #tests about number only
    test("1", 1)
    test("10", 10)
    test("1.0", 1.0)
    test("10.2", 10.2)

    #tests about plus only
    test("1+2", 3)
    test("1+2+3", 6)
    test("1.0+1+2", 4)
    test("1.0+1.0+3.0", 5.0)

    #tests about minus only
    test("5-1-2", 2)
    test("2-1.0", 1)
    test("2.0-1.0", 1.0)
    test("10.0-5.6-2", 2.4)

    #tests about multiply only
    test("2*3", 6)
    test("2.5*2", 5.0)
    test("2.6*3.5", 9.1)
    test("2.5*2*6", 30)

    #tests about divide only
    test("6/2", 3)
    test("5/2", 2.5)
    test("2.5/5", 0.5)
    test("2.5/0.5", 5)
    test("2.5/0.5/5", 1)

    #tests about plus and minus
    test("1+4-2", 3)
    test("2.0+6-2.5", 5.5)

    #tests about multiply and divide
    test("2*6/3", 4)
    test("5.5*6/0.5", 66)


    #tests about arithmetic operations
    test("2*6/3+4+1-2/2", 8)
    test("5/2+3.5-1+6/2.5", 7.4)

    #tests including parenthesis
    test("(3.0+4*(2-1))/5", 1.4)
    test("3.0+4*(2-1)", 7.0)
    test("(3+4)/(9-2)", 1)
    test("((3.5-0.5)-2)*10/(4+1)", 2)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer
