from collections import deque

import numpy as np


class Computer:
    def __init__(self, instructions, program):
        self.memory = np.zeros(2**15, dtype=np.uint16)
        self.memory[:len(program)] = program
        self.registers = np.zeros(8, dtype=np.uint16)
        self.stack = deque()
        self.pointer = np.uint16(0)
        self.caught = instructions

    out_stream = ''

    def normalise_slot(self, num):
        return self.registers[num - 32768] if num > 32767 else num

    def normalise_slots(self, *nums):
        return [self.normalise_slot(num) for num in nums]

    def add(self, a: np.uint16, b: np.uint16, c: np.uint16):
        b, c = self.normalise_slots(b, c)
        answer = (b+c) % 32768
        self._write_to(a, answer)
        self.pointer += 4

    def halt(self):
        raise StopIteration

    def set(self, a, b):
        """
        set register a to the value of b
        """
        self.registers[a-32768] = self.normalise_slot(b)
        self.pointer += 3

    def push(self, a):
        a = self.normalise_slot(a)
        self.stack.append(a)
        self.pointer += 2

    def pop(self, a):
        element = self.stack.pop()
        self._write_to(a, element)
        self.pointer += 2

    def _write_to(self, address, value):
        if address < 32768:
            self.memory[address] = value
        else:
            self.registers[address - 32768] = value

    def eq(self, a, b, c):
        b, c = self.normalise_slots(b, c)
        self._write_to(a, b == c)
        self.pointer += 4

    def out(self, a):
        self.out_stream += chr(self.normalise_slot(a))
        print(a, flush=False, end='')
        self.pointer += 2

    def gt(self, a, b, c):
        b, c = self.normalise_slots(b, c)
        self._write_to(a, b > c)
        self.pointer += 4

    def jmp(self, a):
        self.pointer = self.normalise_slot(a)

    def jt(self, a, b):
        a, b = self.normalise_slots(a, b)
        self.pointer = b if a else self.pointer + 3

    def jf(self, a, b):
        a, b = self.normalise_slots(a, b)
        self.pointer = self.pointer + 3 if a else b

    def mult(self, a, b, c):
        b, c = self.normalise_slots(b, c)
        answer = np.multiply(b, c) % 32768
        self._write_to(a, answer)
        self.pointer += 4

    def mod(self, a, b, c):
        b, c = self.normalise_slots(b, c)
        self._write_to(a, b % c)
        self.pointer += 4

    def and_(self, a, b, c):
        b, c = self.normalise_slots(b, c)
        self._write_to(a, b & c)
        self.pointer += 4

    def or_(self, a, b, c):
        b, c = self.normalise_slots(b, c)
        self._write_to(a, b | c)
        self.pointer += 4

    def not_(self, a, b):
        b = self.normalise_slot(b)
        as_15 = np.binary_repr(b, width=15)
        inv = ''.join('1' if x == '0' else '0' for x in as_15)
        self._write_to(a, int(inv, 2))
        self.pointer += 3

    def rmem(self, a, b):
        """
        read memory at address b and write it to a.
        If b > 38768, look at the relevant register and use that
        address in the memory.
        """
        b = self.normalise_slot(b)
        b = self.memory[b]
        self._write_to(a, b)
        self.pointer += 3

    def wmem(self, a, b):
        """
        Write the value from b into memory at address a
        """
        a, b = self.normalise_slots(a, b)
        self._write_to(a, b)
        self.pointer += 3

    def call(self, a):
        self.stack.append(self.pointer+2)
        self.jmp(a)

    def ret(self):
        item = self.stack.pop()
        self.jmp(item)

    def in_(self, a, char):
        self._write_to(a, ord(char))
        self.pointer += 2

    def noop(self):
        self.pointer += 1

    def memory_at_offset(self, offset) -> int:
        return self.memory[self.pointer+offset]

    def memory_at_offsets(self, *offsets):
        return [self.memory_at_offset(offset) for offset in offsets]

    def step(self):
        match self.memory[self.pointer]:
            case 0:
                self.halt()
            case 1:
                self.set(*self.memory_at_offsets(1, 2))
            case 2:
                self.push(self.memory_at_offset(1))
            case 3:
                self.pop(self.memory_at_offset(1))
            case 4:
                self.eq(*self.memory_at_offsets(1, 2, 3))
            case 5:
                self.gt(*self.memory_at_offsets(1, 2, 3))
            case 6:
                self.jmp(self.memory_at_offset(1))
            case 7:
                self.jt(*self.memory_at_offsets(1, 2))
            case 8:
                self.jf(*self.memory_at_offsets(1, 2))
            case 9:
                self.add(*self.memory_at_offsets(1, 2, 3))
            case 10:
                self.mult(*self.memory_at_offsets(1, 2, 3))
            case 11:
                self.mod(*self.memory_at_offsets(1, 2, 3))
            case 12:
                self.and_(*self.memory_at_offsets(1, 2, 3))
            case 13:
                self.or_(*self.memory_at_offsets(1, 2, 3))
            case 14:
                self.not_(*self.memory_at_offsets(1, 2))
            case 15:
                self.rmem(*self.memory_at_offsets(1, 2))
            case 16:
                self.wmem(*self.memory_at_offsets(1, 2))
            case 17:
                self.call(self.memory_at_offset(1))
            case 18:
                self.ret()
            case 19:
                self.out(self.memory_at_offset(1))
            case 20:
                if not self.caught:
                    self.caught = list(input()) + ['\n']
                next_char = self.caught.pop(0)
                self.in_(self.memory_at_offset(1), next_char)
            case 21:
                self.noop()

    def run(self, steps=1_000_000):
        for _ in range(steps):
            self.step()
