import elementClasses

gate = elementClasses.AndGate('And gate 1')

gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput(1)
gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput(0)
gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput(0)
gate.setInput(1)
gate.pulse()
assert gate.outputHasFired

gate = elementClasses.OrGate('Or gate 1')

gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput(1)
gate.pulse()
assert gate.outputHasFired

gate.reset()
gate.setInput(0)
gate.pulse()
assert gate.outputHasFired

gate.reset()
gate.setInput(0)
gate.setInput(1)
gate.pulse()
assert gate.outputHasFired


gate = elementClasses.XorGate('XOr gate 1')

gate.pulse()
assert not gate.outputHasFired

gate.reset()
gate.setInput(1)
gate.pulse()
assert gate.outputHasFired

gate.reset()
gate.setInput(0)
gate.pulse()
assert gate.outputHasFired


print '-------------'
gate.reset()
gate.setInput(0)
gate.setInput(1)
gate.pulse()
assert not gate.outputHasFired



