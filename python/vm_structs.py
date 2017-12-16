from collections import namedtuple

Token = namedtuple('Token', 'raw, value, stbyte, ndbyte')

OP_ARITY = {
    0: 0, 1: 2, 2: 1, 3: 1, 4: 3, 5: 3,
    6: 1, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3,
    12: 3, 13: 3, 14: 2, 15: 2, 16: 2,
    17: 1, 18: 0, 19: 1, 20: 1, 21: 0
}


class TokenTree:
    @classmethod
    def from_bytes(clx, b):
        return TokenTree(clx.tokenize(b))

    @staticmethod
    def parse_token(b):
        value = int.from_bytes(b, byteorder='little')
        stbyte, ndbyte = (value << 8) >> 8, (value >> 8)
        return Token(b, value, stbyte, ndbyte)

    @classmethod
    def tokenize(clx, rawcode, token_len=2):
        return [clx.parse_token(rawcode[i:i + token_len])
                for i in range(0, len(rawcode), token_len)]

    def __init__(self, tokens, start=0):
        self.tokens = tokens
        self.position = 0

    def get_op_with_args(self):
        op = self.take(1)[0]
        args = self.take(OP_ARITY[op.value])
        return op, args

    def take(self, n=1):
        r = self.tokens[self.position:self.position + n]
        self.position += n
        return r

    def check(self, n=1):
        return self.tokens[self.position:self.position + n]

    def has_next(self):
        return self.position != len(self.tokens)

    def nth(self, n):
        return self.tokens[n]

    def jump_to(self, p):
        self.position = p

    def update_token(self, pos, val):
        stbyte, ndbyte = (val << 8) >> 8, (val >> 8)
        self.tokens[pos] = Token(b'', val, stbyte, ndbyte)


class Memory:
    def __init__(self):
        self.stack = []
        self.registers = {}
