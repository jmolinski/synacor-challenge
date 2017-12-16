from operations import OPERATIONS
from itertools import count
from exceptions import TerminateExecution
from vm_structs import TokenTree, Memory

DEBUG = False
DEBUG_ON_FOR = ()


def run(rawcode):
    tree = TokenTree.from_bytes(rawcode)
    memory = Memory()

    try:
        for op_token, args in (tree.get_op_with_args() for _ in count()):
            if DEBUG or op_token.value in DEBUG_ON_FOR:
                print(op_token.value, [a.value for a in args],
                      memory.registers, memory.stack)
            OPERATIONS[op_token.value](*args, tree=tree, memory=memory)
    except TerminateExecution:
        return
    except:
        raise


if __name__ == '__main__':
    with open('../challenge.bin', 'rb') as f:
        rawcode = f.read()
    run(rawcode)
