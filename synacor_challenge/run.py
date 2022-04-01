import numpy as np
from computer import Computer
from synacor_challenge.maze_instructions import instructions

program = np.fromfile('../challenge.bin', dtype=np.uint16)
comp = Computer(instructions, program)

# comp.load_program(program)
comp.run(911265)
# comp.registers[7] = 100
# comp.run(127)
# while True:
#     if comp.pointer in [521, 5451, 5522, 6042]:
#         print(comp.pointer)
#         break
#     comp.step()