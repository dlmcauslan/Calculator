# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 11:06:17 2016

A scientific calculator that accepts inputs of +-*/^% as well as ().
Also accepts trigonometric inputs (sin, cos, tan, asin, acos, atan), sqrt, log, ln and abs functions.
Accepts exponential notation in the format 2.5 EXP 7 (not case sensitive) 

@author: dmcauslan

modified 28/09/2016:
    * Calculator now accepts negative numbers as inputs
    * Calculator now checks if there's unmatched brackets and brings up an error
    * Calculator now brings up an error if the number of numerical inputs is incorrect
    * Calculator now accpets % to perform modulo calculation
    * Calculator now parses special functions - toPostfix just passes if it finds a fn atm.
modified 29/09/2016:
    * Calculator now accepts trigonometric functions, sqrt(), log(), ln(), abs as inputs
    * Now accepts pi and e as special numerical inputs
    * Have implemented scientific notation with exp.
    
To Do:
    Include yth root function, factorial function
    Include use of ans, to recall the answer of the last calculation
    Split parseInput() into several different functions.    
    Tidy up functions!
    Create .exe    
    Create GUI
"""

import operator as op
import string
import math as m

def isFloat(value):
    """ Checks whether a number is a float"""        
    try:
        float(value)
        return True
    except ValueError:
        return False


class Calculator(object):
    # Dictionary of their operators and the corresponding operation and their precedence
    operators = {'+': (op.add,0), '-': (op.sub,0), 
              '*': (op.mul,1), '/': (op.truediv,1), 
              '^': (op.pow,2), '%': (op.mod,3) }
    # Dictionary of the available special functions for use          
    functions = {'sqrt': m.sqrt, 'log': m.log10, 'ln': m.log, 'abs':  m.fabs,
                 'sin': m.sin, 'cos': m.cos, 'tan': m.tan,
                 'asin': m.asin, 'acos': m.acos, 'atan': m.atan}
    # Special numbers
    specialNumbers = {'pi': m.pi, 'e': m.e}
   
    
    def evaluate(self, calcStr):
        """ Main method of the calculator that performs all of the calculation steps, returns the final answer"""
        # parse string so that it is broken up into the individual pieces
        newStr = self.parseInput(calcStr)
        if newStr == "Error":
            return "Please enter a valid input!"
        # convert the input to postfix notation
        postfix = self.toPostfix(newStr)
        if postfix == "Unmatched Error":
            return "Your input has unmatched brackets!"
        print(postfix)
        # Then perform the calculation and return the answer
        answer = self.postfixCalc(postfix)
        if answer == "Too Many Error":
            return "Your input has too many numbers!"
        if answer == "Too Few Error":
            return "Your input has too few numbers!"
        return answer

  
    def toPostfix (self,infix):
        """Takes in an array of characters in infix notation and returns an array of the same
        expression in postfix notation."""
        postfix = []
        stack = []
        # Loop over characters in the input string
        for char in infix:
            # If char is a number add it to postfix
            if isFloat(char):
#                postfix.append('{}'.format(float(char)))
                postfix.append(char)
            # If its a special number add it to postfix
            elif char in Calculator.specialNumbers:
                postfix.append(char)
            # If char is a function push it onto the stack
            elif char in Calculator.functions:
                stack.append(char)
            # If char is an operator O
            elif char in Calculator.operators:
                # While there is an operator, P, on the top of stack
                while len(stack)>0 and stack[-1] in Calculator.operators:
                    stackTop = stack[-1]
                    precChar = Calculator.operators[char][1]
                    precStackTop = Calculator.operators[stackTop][1]
                    # If O in -?+* and its precedence is <= P, pop P off stack
                    if char in Calculator.operators and precChar <= precStackTop:
                        postfix.append(stack.pop())
                    else:
                        break
                # Push O onto stack
                stack.append(char)
            # If char is (, push it onto the stack
            elif char == '(':
                stack.append(char)
            # If char is )
            elif char == ')':
                # If the size of the stack reaches 0 without finding a ( there are unmatched brackets.
                if len(stack) == 0:
                    return "Unmatched Error"
                # While top of stack isn't ( pop operators off the top of the stack
                while stack[-1] != '(':
                    postfix.append(stack.pop())
                    # If the size of the stack reaches 0 without finding a ( there are unmatched brackets.
                    if len(stack) == 0:
                        return "Unmatched Error"
                # Pop ( off the stack, but not onto output queue
                stack.pop()
                # If the token at the top of the stack is a function pop it off the stack and add to postfix
                if len(stack) > 0 and stack[-1] in Calculator.functions:
                    postfix.append(stack.pop())
        # Finally pop all the operators off the stack onto postfix
        while len(stack)>0:
            # If the operator on the top of the stack is () then there are unmatched brackets
            if stack[-1] in '()':
                return "Unmatched Error"
            postfix.append(stack.pop())
        return postfix
    
    def postfixCalc(self,tokens):
        """ Takes a postfix expression as a list and evaluates it """
        if len(tokens) == 0:
            return 0
        stack = []
        # while expr is not empty
        while len(tokens)>0:
            toke = tokens.pop(0)
            # if token is a number push it onto the stack
            if isFloat(toke):
                stack.append(float(toke))
            # if token is a special number push it onto the stack
            elif toke in Calculator.specialNumbers:
                stack.append(Calculator.specialNumbers[toke])
            else:
                # Operators take 2 inputs, functions take 1 input
                if toke in Calculator.operators:
                    n = 2
                elif toke in Calculator.functions:
                    n = 1
                # If the length of the stack is less than the required number of operators the user has not 
                # input enough values.
                if len(stack)<n:
                    return "Too Few Error"
                # Pop the top n numbers from the stack
                popedVals = []
                for i in range(n):
                    popedVals.append(stack.pop())
                # Evaluate the operator using the number(s) that were popped, and push back onto the stack
                if n == 2:
                    stack.append(Calculator.operators[toke][0](popedVals[1],popedVals[0]))
                elif n == 1:
                    stack.append(Calculator.functions[toke](popedVals[0]))
        # If there is more than one value left on the stack the user has input too many values
        if len(stack) > 1:
            return "Too Many Error"
        # Return the value on the stack (should only be 1 value left)
        return stack[-1]

    
    def negativeCheck(self, stringArray):
        ''' Loops over stringArray and checks to see whether minus symbols should correspond to negative numbers'''
        newStringArray = []
        n = 0
        while n < len(stringArray):
            # If the first character is a - sign then the next charater should be a negative number
            if n == 0:
                if stringArray[n]=='-':
                    newStringArray.append(stringArray[n]+stringArray[n+1])
                    n+=1
                else:
                    newStringArray.append(stringArray[n])
            # If the character is a - sign and it is preceded by an operator or ( or exp then the next character should be a negative number
            elif stringArray[n]=='-' and (stringArray[n-1] in Calculator.operators or stringArray[n-1] == '(' or stringArray[n-1] == 'exp'):
                newStringArray.append(stringArray[n]+stringArray[n+1])
                n+=1           
            else:
                newStringArray.append(stringArray[n])
            n+=1
        return newStringArray
    
    
    def scientificNotationCheck(self, stringArray):
        ''' Loop over stringArray and see if it any of the numbers are in scientific notation'''
        newStringArray=[]
        n = 0
        while n < len(stringArray):
            # If the character is 'exp' and it has a number either side (including negatives) then change the last item in the
            # list to aeb where a is the first number, b is the second, else throw an error                        
            if stringArray[n] == 'exp':
                try:
                    newStringArray[-1] = str(float('{}e{}'.format(newStringArray[-1], stringArray[n+1])))
                    n+=1
                except ValueError:
                    return "Error"
                except IndexError:
                    return "Error"
            else:
                newStringArray.append(stringArray[n])
            n+=1
        return newStringArray
    
    
    def parseInput(self,calcStr):
        """ Takes the user input, checks to see whether it's valid and returns it as an array
        split into the indivual pieces """
        stringArray = []
        tmpString = ''
        n = 0
        while n < len(calcStr):
            char = calcStr[n]
            # If its a number or '.' add it to a temporary string
            if char in string.digits or char == '.':
                tmpString+=char
            else:
                if tmpString != '':
                    stringArray.append(tmpString)
                    tmpString=''
                # If its a space, pass
                if char == ' ':
                    pass
                # If its a special character, add it to the string array
                elif char in Calculator.operators or char in '()':        
                    stringArray.append(char)           
                # If its a letter, check to see whether its a function
                elif char in string.ascii_letters:
                    fnString = ''
                    foundFn = False
                    # Look ahead
                    while foundFn == False and n < len(calcStr) and calcStr[n] in string.ascii_letters:
                        fnString+=calcStr[n].lower()
                        n+=1
                        # if it finds the letter e, look ahead to check ahead to see whether the next letter is x
                        # otherwise exp will always get picked up as the number e - then throw an error.
                        if fnString == 'e' and n < len(calcStr) and calcStr[n].lower()=='x':
                            pass
                        # If it finds a string thats a function, a special number or exp, break the loop
                        elif fnString in Calculator.functions or fnString == 'exp' or fnString in Calculator.specialNumbers:
                            # Add the string to stringArr
                            print(fnString)
                            stringArray.append(fnString)
                            foundFn = True
                    # If it finds a string that's not a function or a special number, return an error
                    if foundFn == False:
                        return "Error"
                    n-=1                    
                # Else its an invalid character
                else:
                    return "Error"
            # If you've reached the end of the array, and tmpString isn't empty add it to the array
            if n == len(calcStr)-1 and tmpString != '':
                stringArray.append(tmpString)
            # Finally increment n by 1
            n+=1
        print(stringArray)

        stringArray = self.negativeCheck(stringArray)
        print(stringArray)
        
        stringArray = self.scientificNotationCheck(stringArray)
        print(stringArray)
        return stringArray

print('What would you like to calculate? (type q to quit)')
while True:
    calcIn = input("--> ")
    if calcIn in'qQ':
        break
    print(Calculator().evaluate(calcIn))

