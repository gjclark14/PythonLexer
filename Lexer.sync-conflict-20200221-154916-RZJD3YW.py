from Token import Token
from enum import Enum
import shlex


class FSM_TRANSITIONS(Enum):
    LETTER = 0
    DIGIT = 1
    SPACE = 2
    PUNCTUATION = 3
    UNKNOWN = -1
    REJECT = 999


class TokenType:
    def __init__(self, token, lexeme, lexemeName):
        self.token = token
        self.lexeme = lexeme
        self.lexemeName = lexemeName


class Lexer:
    table = [
        #    L  D  SP P state                   idx backup
        [1, 3, 0, 4],  # starting state     0   P with 2 should be a non back up state
        [1, 1, 2, 2],  # in identifier      1
        [0, 0, 0, 0],  # end identifier     2   y
        [4, 3, 4, 4],  # in number          3
        [0, 0, 0, 0]  # end number         4   n
    ]

    finalStates = [2, 4]
    backUpStates = [2]

    def __init__(self, inputString):
        self.str = inputString
        self.strings = shlex.split(inputString)

    @staticmethod
    def isSeparator(c):
        return c in Token.SEPARATORS

    @staticmethod
    def charToCol(c):
        if c.isalpha():
            return 0
        if c.isdigit():
            return 1
        if c.isspace():
            return 2
        if Lexer.isSeparator(c):
            return 3

        return 999

    def isFinalState(self, state):
        return state in Lexer.finalStates

    # state and character as input
    # will be a switch on currentState
    def lex(self, string):

        accessToken = TokenType(0, 0, 0)
        lexemes = []

        lexeme = ""

        currentState = 0
        previousState = 0
        LEN = len(string)

        i = 0
        while i < LEN:
            char = string[i]
            col = Lexer.charToCol(string[i])
            currentState = Lexer.table[currentState][col]

            lexeme = ""
            if not char.isspace():
                lexeme = lexeme + char

            if self.isFinalState(currentState):
                print(lexeme)
                lexeme = ""

            i += 1

    def isBackUpState(self, state):
        return state in self.backUpStates

    def getLexemeName(self, lexeme):
        if (lexeme == FSM_TRANSITIONS.LETTER):
            return "LETTER"
        if (lexeme == FSM_TRANSITIONS.DIGIT):
            return "DIGIT"
        if (lexeme == FSM_TRANSITIONS.SPACE):
            return "SPACE"
        if (lexeme == FSM_TRANSITIONS.PUNCTUATION):
            return "PUNCTUATION"
        return "ERROR"


if __name__ == '__main__':
    l = Lexer("int")
    l.lex("int a b c ")

#    print('char', str(i+1).rjust(3, ' '), ':', char)
