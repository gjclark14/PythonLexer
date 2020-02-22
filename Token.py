#

TT_INT = 'TT_INT'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'




class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1 # current position
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

#        while self.current_char != None:
            #if self.current_char.isspace():
            #    self.advance()
            #elif:
            #    return

        return tokens


















