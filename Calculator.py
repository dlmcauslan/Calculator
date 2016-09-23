# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 11:06:17 2016

@author: dmcauslan

To Do:
    Make sure negative signs work    
    Check for invalid inputs, such as unmatched brackets, numbers with no operator betwen them
    Create .exe    
    Extend to scientific calculator
    Create GUI
"""

import operator as op
import string

class Calculator(object):
    def evaluate(self, calcStr):
        # parse string so that it is broken up into the individual pieces
        newStr = self.parseInput(calcStr)
        if newStr == "Error":
            return "Please enter a valid input!"
        # convert the input to postfix notation
        postfix = self.toPostfix(newStr)
#        print(postfix)
        # Then perform the calculation and return the answer
        return self.postfixCalc(postfix)

    def toPostfix (self,infix):
        """Convert infix to postfix"""
        postfix = ''
        stack = []
        ops = '+-*/^'
        # Loop over characters in the input string
        for char in infix:
            # If char is a number add it to postfix
            try:
                postfix+='{} '.format(float(char))
            except ValueError:
                pass      
            # If char is an operator O
            if char in ops:
                # While there is an operator, P, on the top of stack
                while len(stack)>0 and stack[-1] in ops:
#                    print(len(stack))
                    stackTop = stack[-1]
                    precChar = ops.index(char)//2
                    precStackTop = ops.index(stackTop)//2
                    # If O in -?+* and its precedence is <= P, pop P off stack
                    if char in ops[:4] and precChar <= precStackTop:
                        postfix+='{} '.format(stack.pop())
                    else:
                        break
                # Push O onto stack
                stack.append(char)
            # If char is (, push it onto the stack
            if char == '(':
                stack.append(char)
            # If char is )
            if char == ')':
               # While top of stack isn't ( pop operators off the top of the stack
                while stack[-1] != '(':
                    postfix+='{} '.format(stack.pop())
                # Pop ( off the stack, but not onto output queue
                stack.pop()
        # Finally pop all the operators off the stack onto postfix
        while len(stack)>0: 
            postfix+='{} '.format(stack.pop())   
        return postfix[:-1]   
    
    def postfixCalc(self,expr):
        if expr == "":
            return 0
        #split by spaces
        tokens = expr.split(" ")
        stack = []
        opDict = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv, '^': op.pow }
        # while expr is not empty
        while len(tokens)>0:
            toke = tokens.pop(0)
            # if token is a number push it onto the stack
            try:
                stack.append(float(toke))
            # Else the token is an operator
            except ValueError:
                # Pop the top 2 numbers from the stack
                y = stack.pop()
                x = stack.pop()
                # Evaluate the operator using the 2 numbers that were popped, and push back onto the stack
                stack.append(opDict[toke](x,y))
        # Return the value on the stack (should only be one left on stack)    
        return stack[-1]
        
    def parseInput(self,calcStr):
        stringArr = []
        tmpString = ''
        for n in range(len(calcStr)):
            char = calcStr[n]
            # If its a space, and tmpString is not empty add tmpString to the array
            if char == ' ':
                if tmpString != '':
                    stringArr.append(tmpString)
                    tmpString=''
            # If its a special character, add it to the string array
            elif char in '+-*/^()':        
                # If tmpstring is not empty add it to the array
                if tmpString != '':
                    stringArr.append(tmpString)
                    tmpString=''
                # Add the special char to the array
                stringArr.append(char)
            # If its a number or '.' add it to a temporary string
            elif char in string.digits or char == '.':
                tmpString+=char
            # Else its an invalid character
            else:
#                raise ValueError("Please enter a valid input!")
                return "Error"
            # If you've reached the end of the array, add tmpString to array
            if n == len(calcStr)-1:
                stringArr.append(tmpString)
            
        return stringArr

print('What would you like to calculate? (type q to quit)')
while True:
    calcIn = input("--> ")
    if calcIn in'qQ':
        break
    print(Calculator().evaluate(calcIn))

