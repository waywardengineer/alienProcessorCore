import elementClasses


def testTruthTable(element, truthTable):
	for row in truthTable:
		element.reset()
		for inputName in row[0]:
			if row[0][inputName]:
				element.setInput(inputName)
		for i in range(element.required_pulses):
			element.fireRead()
		for outputName in row[1]:
			if row[1][outputName]:
				assert element.outputsHaveTriggered[outputName]
			else:
				assert not element.outputsHaveTriggered[outputName]

testTruthTable(
	elementClasses.AndGate('And gate 1'),
	[
		({'A': 0, 'B': 0}, {'out': 0}),
		({'A': 1, 'B': 0}, {'out': 0}),
		({'A': 0, 'B': 1}, {'out': 0}),
		({'A': 1, 'B': 1}, {'out': 1}),
	]
)

testTruthTable(
	elementClasses.OrGate('Or gate 1'),
	[
		({'A': 0, 'B': 0}, {'out': 0}),
		({'A': 1, 'B': 0}, {'out': 1}),
		({'A': 0, 'B': 1}, {'out': 1}),
		({'A': 1, 'B': 1}, {'out': 1}),
	]
)

testTruthTable(
	elementClasses.XorGate('Xor gate 1'),
	[
		({'A': 0, 'B': 0}, {'out': 0}),
		({'A': 1, 'B': 0}, {'out': 1}),
		({'A': 0, 'B': 1}, {'out': 1}),
		({'A': 1, 'B': 1}, {'out': 0}),
	]
)

testTruthTable(
	elementClasses.HalfAdder('Half adder 1'),
	[
		({'A': 0, 'B': 0}, {'sum': 0, 'carry': 0}),
		({'A': 1, 'B': 0}, {'sum': 1, 'carry': 0}),
		({'A': 0, 'B': 1}, {'sum': 1, 'carry': 0}),
		({'A': 1, 'B': 1}, {'sum': 0, 'carry': 1}),
	]
)

testTruthTable(
	elementClasses.FullAdder('Full adder 1'),
	[
		({'carry_in': 0, 'B': 0, 'A': 0}, {'sum': 0, 'carry_out': 0}),
		({'carry_in': 0, 'B': 0, 'A': 1}, {'sum': 1, 'carry_out': 0}),
		({'carry_in': 0, 'B': 1, 'A': 0}, {'sum': 1, 'carry_out': 0}),
		({'carry_in': 0, 'B': 1, 'A': 1}, {'sum': 0, 'carry_out': 1}),
		({'carry_in': 1, 'B': 0, 'A': 0}, {'sum': 1, 'carry_out': 0}),
		({'carry_in': 1, 'B': 0, 'A': 1}, {'sum': 0, 'carry_out': 1}),
		({'carry_in': 1, 'B': 1, 'A': 0}, {'sum': 0, 'carry_out': 1}),
		({'carry_in': 1, 'B': 1, 'A': 1}, {'sum': 1, 'carry_out': 1}),
	]
)
