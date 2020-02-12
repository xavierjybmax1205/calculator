import math
class Calculator:
    class stack:
        class node:
            def __init__(self, val, nextNode):
                    self.value = val
                    self.nextNode = nextNode            
        def __init__(self):
            self.top = None
            self.size = 0
        def __len__(self):
            return self.size  
        def push(self, val):
            self.top = self.node(val,self.top)
            self.size = self.size + 1
        def pop(self):
            value = None
            if self.size ==0:
                return "error"
            if self.size >0:
                value = self.top.value
                self.top = self.top.nextNode
                self.size = self.size -1
            return value

    def isEqual(self, obj1, obj2):
        return obj1 == obj2
    def isNotEqual(self, obj1, obj2):
        return obj1 != obj2
    def isGreaterOrEqual(self, obj1, obj2):
        return obj1 >= obj2
    def isSmallerOrEqual(self, obj1, obj2):
        return obj1 <= obj2
    def isInArray(self, obj, array):
        return obj in array
    def concatString(self, string1, string2):
        return string1 + string2
    def replaceString(self, string, old, new):
        return string.replace(old, new)
    
    def splitString(self, string, symble):
        return string.split(symble)
    def increment(self, number):
        return number + 1
    def returnItSelf(self, it):
        return it
            

    def exeOpr(self, num1, opr, num2):
        result = None
        if self.isEqual(opr, "+"):
            result = num1+num2
        elif self.isEqual(opr, "-"):
            result = num1-num2
        elif self.isEqual(opr, "*"):
            result = num1*num2
        elif self.isEqual(opr, "/"):
            result = num1/num2
        elif self.isEqual(opr, "^"):
            result = num1**num2
        return result
        
    def findNextOpr(self, s):
        if len(s)<=0 or not isinstance(s,str):
            print("type mimatch error: findNextOpr")
            return "type mimatch error: findNextOpr"        
        result = -1
        for (position, obj) in enumerate(list(s)):
            if self.isInArray(obj, ['+', '-', '*', '/']):
                result = position
                break

        if self.isEqual(result, -1):
            return -1
        else:
            return result

        return result
    def isNumber(self, s):
        if len(s)==0 or not isinstance(s, str):
            print("type mismatch error: isNumber")
            return "type mismatch error: isNumber"
        try:
            float(s.strip())
            return True
        except ValueError:
            return False
     

    def isVariable(self, s):
        s = s.strip()
        if self.isInArray(s, self.varDic) == True:
            return True
        else:
            return self.isInArray(s, self.varDic)

    def getNextNumber(self, expr, pos):
        #expr is a given arithmetic formula in string
        #pos = start position in expr
        #1st returned value = the next number (None if N/A)
        #2nd returned value = the next operator (None if N/A)
        #3rd retruned value = the next operator position (None if N/A)
        if len(expr)==0 or not isinstance(expr, str) or pos<0 or pos>=len(expr) or not isinstance(pos, int):
            print("type mismatch error: getNextNumber")
            return None, None, "type mismatch error: getNextNumber"
        #--- function code starts ---#
        positionOfNextOperator = self.findNextOpr(expr[pos:])
        if self.isEqual(positionOfNextOperator, -1):
            positionOfNextOperator, nextOperator, nextNumber = None, None, expr[pos:]
        elif self.isEqual(positionOfNextOperator, 0):
            pos = pos + 1
            positionOfNextOperator = self.findNextOpr(expr[pos:])
            if self.isEqual(positionOfNextOperator, -1):
                positionOfNextOperator, nextOperator, nextNumber = None, None, expr[pos-1:]
            else:
                positionOfNextOperator = positionOfNextOperator + pos
                nextOperator = expr[positionOfNextOperator]
                nextNumber = self.concatString("-", expr[pos:positionOfNextOperator])
        else:
            positionOfNextOperator = self.returnItSelf(positionOfNextOperator + pos)
            nextOperator = self.returnItSelf(expr[positionOfNextOperator])
            nextNumber = self.returnItSelf(expr[pos:positionOfNextOperator])       

        if not self.isNumber(nextNumber):
            nextNumber = self.returnItSelf(None)
        else:
            nextNumber = self.returnItSelf(float(nextNumber))

        return (nextNumber, nextOperator, positionOfNextOperator)

    def __init__(self):
        self.lines, self.varDic, self.varList, self.functDef = [], {}, [], '''
        sqrt x: math.sqrt(x) ;

        exp  x: math.exp(x) ;

        sin  x: math.sin(x) ;

        cos  x: math.cos(x) ;

        tan  x: math.tan(x) ;

        ln   x: math.log(x) ;

        lg   x: math.log(x) / math.log(2) ;

        mod x, y: x – y * math.floor(x/y)

        '''
        self.functDic = {}
        self.setFunct()

    def setFunct(self):
        dic1 = {
            'sqrt': 'x: math.sqrt(x)',
            'exp': 'x: math.exp(x)',
            'sin': 'x: math.sin(x)',
            'cos': 'x: math.cos(x)',
        }
        dic2 = {
            'tan': 'x: math.cos(x)',
            'ln': 'x: math.log(x)',
            'lg': 'x: math.log(x) / math.log(2)',
            'round': 'x, d: round(x, d)',
            'mod': 'x, y: x - y * math.floor(x/y)'
        }
        self.functDic = {**dic1, **dic2}

    def findFunctParen(self, expr):
        found, funct, lIndex, nameList = False, '', -1, self.returnItSelf(["sqrt","exp","sin","cos","tan","ln","lg","round","mod"])
        for name in nameList:
            if expr.find(name) >=0:
                found, funct = True, name
                lIndex = expr.find(name)
                break
        if (found):
            lbC, endIndex = 0, lIndex
            for (index, char) in enumerate(expr[lIndex:]):
                if char == "(":
                    lbC = self.increment(lbC)
                if char == ")":
                    lbC -=1
                    if lbC == 0:
                        endIndex += index
                        break
            return lIndex, endIndex, funct
        else:
            if expr.find("(") >= 0:
                lIndex = expr.find("(")
                rIndex = expr.find(")")
                return lIndex, rIndex, None
            return None, None, None

    def getLines(self, expr):
        expr = self.replaceString(expr, " ", "")
        l1 = self.splitString(expr, ";")
        for (index, l) in enumerate(l1):
            if self.isGreaterOrEqual(l.find("return"), 0):
                l2 = self.replaceString(l, "return", "")
                l2 = ["__return__", l2]
                self.varDic[l2[0]] = l2[1]
            else:
                l2 = self.splitString(l, "=")
                if l2[0] == 'return':
                    l2[0] = "__return__"
                elif len(l.strip()) != 0:
                    self.varDic[l2[0]] = l2[1]
                    self.varList.append(l2[0])
            l1[index] = l2
            
        self.lines = l1
 

    def _calc(self, expr):
        expr = self.handleExpo(expr)
        if expr == None:
            return "2 error"

        elif self.isNumber(expr):
            return float(expr)
        
        if len(expr)<=0 or not isinstance(expr,str):
            print("argument error: line A in eval_expr")        #Line A
            return "argument error: line A in eval_expr"

        newNumber, newOpr, oprPos = self.getNextNumber(expr, 0)
        if self.isEqual(newNumber, None):
            #print("invalid expression", expr)
            #print(newNumber, newOpr, oprPos)
            print("input formula error: line B in eval_expr")   #Line B
            return "error"
        elif self.isEqual(newOpr, None):
            return newNumber
        elif self.isEqual(newOpr, "+") or self.isEqual(newOpr, "-"):
            mode, addResult, mulResult = "add", newNumber, None
        elif self.isEqual(newOpr, "*") or self.isEqual(newOpr, "/"):
            mode, addResult, mulResult = "mul", 0, newNumber
            
        pos, opr=self.increment(oprPos), newOpr

        while True:
            #--- code while loop ---#
            nextNumber, nextOpr, nextOprPos = self.getNextNumber(expr, pos)
            if self.isEqual(nextOpr, "+") or self.isEqual(nextOpr, "-"):
                nextMode = "add"
            elif self.isEqual(nextOpr, "*") or self.isEqual(nextOpr, "/"):
                nextMode = "mul"
            else:
                nextMode = None
            if self.isEqual(nextNumber, None):
                if self.isEqual(mode, "add"):
                    return addResult
                else:
                    return mulResult
            
            elif self.isEqual(mode, "add") and self.isEqual(nextMode, "add"):
                addResult = self.exeOpr(addResult, opr, nextNumber)
                return self._calcHW3(str(addResult) + expr[nextOprPos:])
            elif self.isEqual(mode, "add") and self.isEqual(nextMode, "mul"):
                if opr == "+":
                    return addResult + calc(expr[pos:])
                elif opr == "-":
                    return addResult + calc("-" + expr[pos:])
            elif self.isEqual(mode, "mul") and self.isEqual(nextMode, "mul"):
                mulResult = self.exeOpr(mulResult, opr, nextNumber)
                return self._calcHW3(str(mulResult) + expr[nextOprPos:])
            elif self.isEqual(mode, "mul") and self.isEqual(nextMode, "add"):
                mulResult = self.exeOpr(mulResult, opr, nextNumber)
                return self._calcHW3(str(mulResult) + expr[nextOprPos:])
            elif self.isEqual(nextMode, None):
                if self.isEqual(mode, "add"):
                    return self.exeOpr(addResult, opr, nextNumber)
                else:
                    return self.exeOpr(mulResult, opr, nextNumber)
            break
            #--- end of function ---#

    def _calcFunctExpr(self, expr):
        # This is calc(expr) of HW3
        expr = self.replaceString(expr, ' ', '')
        #step 1check syntex
        checkSyntexResult = self.checkSyntex(expr) 
        if (self.isNotEqual(checkSyntexResult, True)):
            return checkSyntexResult

        while self.findFunctParen(expr)[2] != None:
            leftEnd = self.findFunctParen(expr)[0]
            rightEnd = self.findFunctParen(expr)[1]
            funct = self.findFunctParen(expr)[2]
            thingsToHandle = expr[leftEnd: rightEnd+1]
            for (functName, functBody) in self.functDic.items():
                exec(functName + "= lambda " + functBody)
            expr = self.replaceString(expr, thingsToHandle, str(eval(thingsToHandle)))
            
        while self.isGreaterOrEqual(expr.find("("), 0):
            s = self.stack()
            for (index, char) in enumerate(expr):
                if self.isEqual(char, "("):
                    s.push(index)
                if self.isEqual(char, ")"):
                    theMostInnerLPIndex, theMostInnrerRPIndex = s.pop(), index
                    result = self._calc(expr[theMostInnerLPIndex+1: theMostInnrerRPIndex])
                    expr = expr.replace(expr[theMostInnerLPIndex:theMostInnrerRPIndex+1], str(result))
                    break

        return self._calc(expr)
    
    def replaceVariables(self, expr):
        replaceFunctDic = {
            'sqrt': '&_$',
            'exp': '&__$',
            'sin': '&___$',
            'cos': '&____$',
            'tan': '&_____$',
            'ln': '&______$',
            'lg': '&_______$',
            'round': '&________$'
        }


        for (key, value) in replaceFunctDic.items():
            expr = self.replaceString(expr, key, value)
        
        while self.isEqual(self.hasVariable(expr), True):
            for (key, value) in self.varDic.items():
                expr = self.replaceString(expr, key, self.concatString(self.concatString("(", str(value)), ")"))

        for (key, value) in replaceFunctDic.items():
            expr = self.replaceString(expr, value, key)

        return expr

    def hasVariable(self, expr):
        for variable in self.varList:
            if self.isEqual(self.isGreaterOrEqual(expr.find(variable), 0), True):
                return self.isGreaterOrEqual(expr.find(variable), 0)
        return False
    
    def calc(self, expr):
        self.__init__()
        expr = self.handleSpecialCase(expr)
        if self.isGreaterOrEqual(expr.find(";"), 0):
            self.getLines(expr)
            if self.isEqual(self.varDic.get("__return__"), None):
                return "error"
            else:
                for (variable, expr) in self.lines:
                    self.varDic[variable] = self.returnItSelf(self._calcFunctExpr(self.returnItSelf(self.replaceVariables(expr))))
                   
        else:
            self.varDic["__return__"] = self.returnItSelf(self._calcFunctExpr(self.returnItSelf(expr)))
        return self.varDic["__return__"] 


    def checkSyntex(self, expr):
        error = self.returnItSelf('')
        lastIsOpr = self.returnItSelf(False)
        operators = self.returnItSelf(['+', '-', '*', '/', '^'])
        LBCount = self.returnItSelf(0)
        RBCount = self.returnItSelf(0)
        for (index, char) in enumerate(expr):
            if self.isEqual(char, "("):
                LBCount = self.increment(LBCount)
            elif self.isEqual(char, ")"):
                RBCount = self.increment(RBCount)
            
            if char in operators:
                if self.isEqual(lastIsOpr, True):
                    error = self.returnItSelf("syntex error")
                    break
                lastIsOpr = self.returnItSelf(True)
            else:
                lastIsOpr = self.returnItSelf(False)

        if self.isNotEqual(LBCount, RBCount):
            error = self.returnItSelf("error")

        if self.isNotEqual(error, ''):
            return self.returnItSelf(error)
        else:
            return self.returnItSelf(True)

    def handleExpo(self, expr):
        error = self.returnItSelf('')
        operators = self.returnItSelf(['+', '-', '*', '/', '^'])
        num = self.returnItSelf('')
        exprList = self.returnItSelf([])
        lastIsOpr = False
        for (index, char) in enumerate(expr):
            if self.isInArray(char, ['+', '-', '*', '/', '^']):
                if self.isEqual(char, "-") and self.isEqual(num, ""):
                    num += char
                    lastIsOpr = False
                else:
                    if self.isEqual(lastIsOpr, True):
                        error = "error"
                        break
                    if self.isNotEqual(num, ''):
                        exprList.append(num)
                        num = ''
                    exprList.append(char)
                    lastIsOpr = True
            else:
                num += char
                if self.isEqual(index, (len(expr) -1)):
                    exprList.append(num)
                lastIsOpr = False
        for (index, char) in enumerate(exprList):
            if self.isEqual(char, "^"):
                result = self.returnItSelf(self.exeOpr(float(exprList[index-1]), char, float(exprList[index+1])))
                exprList[index-1] = self.returnItSelf(" ")
                exprList[index] = self.returnItSelf(" ")
                exprList[index+1] = self.returnItSelf(" ")
                exprList.insert(index-1, str(result))
                
        exprList  = self.returnItSelf([x for x in exprList if x != " "])
        while self.isInArray("*", exprList) or self.isInArray("/", exprList):
            for (index, char) in enumerate(exprList):
                if self.isEqual(char, "*") or self.isEqual(char, "/") :
                    result = self.returnItSelf(self.exeOpr(float(exprList[index-1]), char, float(exprList[index+1])))
                    exprList[index-1] = self.returnItSelf(" ")
                    exprList[index] = self.returnItSelf(" ")
                    exprList[index+1] = self.returnItSelf(" ")
                    exprList.insert(index-1, str(result))
                    exprList  = self.returnItSelf([x for x in exprList if x != " "])
                    break

                
        if self.isNotEqual(error, ''):
            return self.returnItSelf(None)
        else:
            return self.replaceString(''.join(exprList), ' ', '')
        
    def handleSpecialCase(self, expr):
        expr = expr.replace(" ", "")
        expr = expr.replace('"', "")
        expr = self.replaceString(expr, " ", "")
        symbles = ['-', '+', '*', '/', '^', '(', ')']
        oprSequenceList = self.returnItSelf([])
        for char in expr:
            if self.isInArray(char, ['-', '+', '*', '/', '^', '(', ')']):
                oprSequenceList.append(char)
        if self.isEqual(oprSequenceList[0], '-') and self.isEqual(oprSequenceList[1], '^') and self.isEqual(expr.find("-"), 0):
            insertIndex = self.increment(expr.find('-'))
            expr=self.returnItSelf(list(expr))
            expr.insert(insertIndex, '(')
            expr.append(')')
            expr = self.returnItSelf(''.join(expr))

        return self.returnItSelf(expr)



c = Calculator()


