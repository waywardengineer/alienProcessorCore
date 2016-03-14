import elementClasses

gate = elementClasses.AndGate('And gate 1')

gate.pulse()
assert not gate.outputsHaveFired['out']

gate.reset()
gate.setInput('B')
gate.pulse()
assert not gate.outputsHaveFired['out']

gate.reset()
gate.setInput('A')
gate.pulse()
assert not gate.outputsHaveFired['out']

gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.pulse()
assert gate.outputsHaveFired['out']

gate = elementClasses.OrGate('Or gate 1')

gate.pulse()
assert not gate.outputsHaveFired['out']

gate.reset()
gate.setInput('B')
gate.pulse()
assert gate.outputsHaveFired['out']

gate.reset()
gate.setInput('A')
gate.pulse()
assert gate.outputsHaveFired['out']

gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.pulse()
assert gate.outputsHaveFired['out']


gate = elementClasses.XorGate('XOr gate 1')

gate.pulse()
assert not gate.outputsHaveFired['out']

gate.reset()
gate.setInput('B')
gate.pulse()
assert gate.outputsHaveFired['out']

gate.reset()
gate.setInput('A')
gate.pulse()
assert gate.outputsHaveFired['out']


gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.pulse()
assert not gate.outputsHaveFired['out']



