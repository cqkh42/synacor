from synacor_challenge.computer import Computer


def test_add():
    c = Computer()
    c.add(32769, 1, 1)
    assert c.registers[1] == 2


def test_rmem_mem_to_mem():
    c = Computer()
    c.memory[0] = 1
    c.rmem(1, 0)
    assert c.memory[1] == 1


def test_rmem_mem_to_reg():
    c = Computer()
    c.memory[0] = 1
    c.rmem(32768, 0)
    assert c.registers[0] == 1


def test_rmem_reg_to_mem():
    c = Computer()
    c.registers[0] = 1
    c.rmem(1, 32768)
    assert c.memory[1] == 1


def test_rmem_reg_to_reg():
    c = Computer()
    c.registers[0] = 1
    c.rmem(32769, 32768)
    assert c.registers[1] == 1
