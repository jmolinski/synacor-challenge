import sys
from exceptions import TerminateExecution

UINT_MAX = 32768


def get_val_or_reg_val(v_token, memory):
    if 0 <= v_token.value <= 32767:
        return v_token.value
    elif 32768 <= v_token.value <= 32775:
        return memory.registers.get(v_token.value, 0)


def save_to_register(value, reg_token, memory):
    memory.registers[reg_token.value] = value


def halt(*args, **kwargs):
    raise TerminateExecution


def set_reg(reg_token, val_token, memory, **kwargs):
    value = get_val_or_reg_val(val_token, memory)
    save_to_register(value, reg_token, memory)


def push(val_token, memory, **kwargs):
    memory.stack.append(get_val_or_reg_val(val_token, memory))


def pop(reg_token, memory, **kwargs):
    save_to_register(memory.stack.pop(), reg_token, memory)


def eq(reg_token, v1_token, v2_token, memory, **kwargs):
    v1 = get_val_or_reg_val(v1_token, memory)
    v2 = get_val_or_reg_val(v2_token, memory)
    save_to_register(int(v1 == v2), reg_token, memory)


def gt(reg_token, v1_token, v2_token, memory, **kwargs):
    v1 = get_val_or_reg_val(v1_token, memory)
    v2 = get_val_or_reg_val(v2_token, memory)
    save_to_register(int(v1 > v2), reg_token, memory)


def jmp(v_token, tree, memory, **kwargs):
    tree.jump_to(get_val_or_reg_val(v_token, memory))


def jt(v_token, dest_token, memory, **kwargs):
    if get_val_or_reg_val(v_token, memory):
        jmp(dest_token, memory=memory, **kwargs)


def jf(v_token, dest_token, memory, **kwargs):
    if get_val_or_reg_val(v_token, memory) == 0:
        jmp(dest_token, memory=memory, **kwargs)


def add(reg_token, v1_token, v2_token, memory, **kwargs):
    v1 = get_val_or_reg_val(v1_token, memory)
    v2 = get_val_or_reg_val(v2_token, memory)
    save_to_register((v1 + v2) % UINT_MAX, reg_token, memory)


def mult(reg_token, v1_token, v2_token, memory, **kwargs):
    v1 = get_val_or_reg_val(v1_token, memory)
    v2 = get_val_or_reg_val(v2_token, memory)
    save_to_register((v1 * v2) % UINT_MAX, reg_token, memory)


def mod(reg_token, v1_token, v2_token, memory, **kwargs):
    v1 = get_val_or_reg_val(v1_token, memory)
    v2 = get_val_or_reg_val(v2_token, memory)
    save_to_register(v1 % v2, reg_token, memory)


def and_op(reg_token, v1_token, v2_token, memory, **kwargs):
    v1 = get_val_or_reg_val(v1_token, memory)
    v2 = get_val_or_reg_val(v2_token, memory)
    save_to_register(v1 & v2, reg_token, memory)


def or_op(reg_token, v1_token, v2_token, memory, **kwargs):
    v1 = get_val_or_reg_val(v1_token, memory)
    v2 = get_val_or_reg_val(v2_token, memory)
    save_to_register(v1 | v2, reg_token, memory)


def not_op(reg_token, v1_token, memory, **kwargs):
    v1 = get_val_or_reg_val(v1_token, memory)
    save_to_register((1 << 15) - 1 - v1, reg_token, memory)


def rmem(reg_token, val_token, memory, tree, **kwargs):
    value = tree.nth(get_val_or_reg_val(val_token, memory)).value
    save_to_register(value, reg_token, memory)


def wmem(mem_token, src_token, memory, tree, **kwargs):
    position = get_val_or_reg_val(mem_token, memory)
    value = get_val_or_reg_val(src_token, memory)
    tree.update_token(position, value)


def call(dest_token, tree, memory, **kwargs):
    memory.stack.append(tree.position)
    tree.jump_to(get_val_or_reg_val(dest_token, memory))


def ret(memory, tree, *args, **kwargs):
    try:
        jump_to = memory.stack.pop()
    except IndexError:
        halt()

    tree.jump_to(jump_to)


def in_op(reg_token, memory, **kwargs):
    save_to_register(ord(sys.stdin.read(1)), reg_token, memory)


def out(char_token, memory, **kwargs):
    print(chr(get_val_or_reg_val(char_token, memory)), end='')


def noop(*args, **kwargs):
    pass


OPERATIONS = {
    0: halt,
    1: set_reg,
    2: push,
    3: pop,
    4: eq,
    5: gt,
    6: jmp,
    7: jt,
    8: jf,
    9: add,
    10: mult,
    11: mod,
    12: and_op,
    13: or_op,
    14: not_op,
    15: rmem,
    16: wmem,
    17: call,
    18: ret,
    19: out,
    20: in_op,
    21: noop,
}
