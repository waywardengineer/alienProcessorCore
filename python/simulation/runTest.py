import elementClasses

gate = elementClasses.AndGate('And gate 1')

gate.fireRead()
assert not gate.outputsHaveTriggered['out']

gate.reset()
gate.setInput('B')
gate.fireRead()
assert not gate.outputsHaveTriggered['out']

gate.reset()
gate.setInput('A')
gate.fireRead()
assert not gate.outputsHaveTriggered['out']

gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.fireRead()
assert gate.outputsHaveTriggered['out']

gate = elementClasses.OrGate('Or gate 1')

gate.fireRead()
assert not gate.outputsHaveTriggered['out']

gate.reset()
gate.setInput('B')
gate.fireRead()
assert gate.outputsHaveTriggered['out']

gate.reset()
gate.setInput('A')
gate.fireRead()
assert gate.outputsHaveTriggered['out']

gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.fireRead()
assert gate.outputsHaveTriggered['out']


gate = elementClasses.XorGate('XOr gate 1')

gate.fireRead()
assert not gate.outputsHaveTriggered['out']

gate.reset()
gate.setInput('B')
gate.fireRead()
assert gate.outputsHaveTriggered['out']

gate.reset()
gate.setInput('A')
gate.fireRead()
assert gate.outputsHaveTriggered['out']


gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.fireRead()
assert not gate.outputsHaveTriggered['out']


gate = elementClasses.HalfAdder('Half adder 1')

gate.fireRead()
assert not gate.outputsHaveTriggered['sum']
assert not gate.outputsHaveTriggered['carry']

gate.reset()
gate.setInput('B')
gate.fireRead()
assert gate.outputsHaveTriggered['sum']
assert not gate.outputsHaveTriggered['carry']

gate.reset()
gate.setInput('A')
gate.fireRead()
assert gate.outputsHaveTriggered['sum']
assert not gate.outputsHaveTriggered['carry']


gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.fireRead()
assert not gate.outputsHaveTriggered['sum']
assert gate.outputsHaveTriggered['carry']



