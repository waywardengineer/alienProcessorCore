import elementClasses

gate = elementClasses.AndGate('And gate 1')

gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput('B')
gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput('A')
gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.pulse()
assert gate.outputHasFired

gate = elementClasses.OrGate('Or gate 1')

gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput('B')
gate.pulse()
assert gate.outputHasFired

gate.reset()
gate.setInput('A')
gate.pulse()
assert gate.outputHasFired

gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.pulse()
assert gate.outputHasFired


gate = elementClasses.XorGate('XOr gate 1')

gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput('B')
gate.pulse()
assert gate.outputHasFired

gate.reset()
gate.setInput('A')
gate.pulse()
assert gate.outputHasFired


gate.reset()
gate.setInput('A')
gate.setInput('B')
gate.pulse()
assert not gate.outputHasFired



