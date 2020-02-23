import shlex
import logging
from enum import Enum

logging.getLogger().setLevel(logging.DEBUG)

class FinalStates(Enum):
    identifier  = 2
    number      = 4
    separator   = 5
    operator    = 6

class TokenLiterals:
    KEYWORDS = {"int", "float", "bool", "true", "false", "if", "else", "then", "endif", "while", "whileend", "do",
                "doend", "for", "forend", "input", "output", "and", "or", "not"}
    SEPARATORS = {"'", "(", ")", "{", "}", "[", "]", ",", ".", ":", ";", " ", "\t", "\n", "\v", "\f", "\r", }
    OPERATORS = {"*", "+", "-", "=", "/", ">", "<", "%"}

class Token:
    def __init__(self, tokenType, lexeme):
        self.tokenType = tokenType
        self.lexeme = lexeme

    def __str__(self):
        return '{:10s} {:1s} {:s}'.format(self.tokenType, ':', self.lexeme)

class Lexer:
    table = [
        #L  D  S  O    state                   idx backup
        [1, 3, 5, 6],  # starting state     0   P with 2 should be a non back up state
        [1, 1, 2, 2],  # in identifier      1
        [0, 0, 0, 0],  # end identifier     2   y
        [4, 3, 4, 4],  # in number          3
        [0, 0, 0, 0],  # end number         4   n
        [0, 0, 0, 0],  # end separator      5
        [0, 0, 0, 0]   # end operator       6
    ]

    finalStates = [2, 4, 5, 6]

    tokens = []

    def __init__(self, inputString):
        self.str = inputString
        self.strings = shlex.split(inputString)

    @staticmethod
    def isSeparator(c):
        return c in TokenLiterals.SEPARATORS

    @staticmethod
    def isOperator(c):
        return c in TokenLiterals.OPERATORS

    @staticmethod
    def charToCol(c):
        if c.isdigit():
            return 1
        if c.isalpha() or c == '$':
            return 0
        if Lexer.isSeparator(c):
            return 2
        if Lexer.isOperator(c):
            return 3

    def addToken(self, tokenType, lexeme):
        self.tokens.append(Token(tokenType, lexeme))

    def lex(self, string):
        state = 0
        LEN = len(string)

        i = 0
        lexeme = ""
        while i < LEN:
            char = string[i]

            if(char == '!'):
                i += 1
                char = string[i]
                while( i < LEN and char != '!'):
                    char = string[i]
                    i += 1
                continue

            if char == '.' and state == 3:
                lexeme += char
                i += 1
                continue

            col = Lexer.charToCol(char)
            state = Lexer.table[state][col]

            if (state == FinalStates.identifier.value):
                i, lexeme, state = self.handleIdentifier(char, col, i, lexeme)
                continue

            if state == FinalStates.number.value:
                i, lexeme, state = self.handleDigit(char, col, i, lexeme)
                continue

            if (state == FinalStates.operator.value):
                i, lexeme, state = self.handleOperator(char, i)
                continue

            if (state == FinalStates.separator.value):
                i, lexeme, state = self.handleSeparator(char, i)
                continue

            lexeme += char
            i += 1

    def handleOperator(self, char, i):
        self.addToken("OPERATOR", char)
        logging.info("OPERATOR: " + char)
        state = 0
        lexeme = ""
        i += 1
        return i, lexeme, state

    def handleSeparator(self, char, i):
        if not char.isspace():
            self.addToken("SEPARATOR", char)
            logging.info("SEPARATOR: " + char)


        state = 0
        lexeme = ""
        i += 1
        return i, lexeme, state

    def handleDigit(self, char, col, i, lexeme):
        self.addToken("NUMBER", lexeme)
        logging.info("NUMBER: " + lexeme)
        # do essentially the same thing that  the identifier is doing with se
        if (col == 2 and not char.isspace()):
            self.addToken("SEPARATOR", char)
            logging.info("SEPARATOR: " + char)
        elif (col == 3):
            self.addToken("OPERATOR", char)
            logging.info("OPERATOR: " + char)
        state = 0
        lexeme = ""
        i += 1
        return i, lexeme, state

    def handleIdentifier(self, char, col, i, lexeme):
        if (lexeme in TokenLiterals.KEYWORDS):
            self.addToken("KEYWORD", lexeme)
            logging.info("KEYWORD: " + lexeme)
        else:
            self.addToken("IDENTIFIER", lexeme)
            logging.info("IDENTIFIER: " + lexeme)
        # separator
        if (col == 2 and not char.isspace()):
            self.addToken("SEPARATOR", char)
            logging.info("SEPARATOR: " + char)
        elif (col == 3):
            self.addToken("OPERATOR", char)
            logging.info("OPERATOR: " + char)
        state = 0
        i += 1
        lexeme = ""
        return i, lexeme, state



    def doSpaces(self, LEN, i, lexeme, string):
        state = 0
        logging.info(lexeme)
        lexeme = ""
        i += 1
        if (i < LEN):
            while (string[i].isspace() and (i) < LEN):
                i += 1
        return i, lexeme, state


if __name__ == '__main__':
    l = Lexer("int")

    # l.nextState("i= 9; ")
    str1 = "int num1, num2, large$\nif(num1 > num2)\n{\n\tlarge = num1$;\n}\nelse\n{\n\tlarge = num2$;\n }"
    str2 = "\nint number;\nnumber = 9.0;\n! Declare and assign a number ! "
    str3 = "n =2; {i=4;} "
    str4 = "2 "
    l.lex(str2)

    for token in l.tokens:
        print(token)

