class LogicElement(object):
	numOutputs = 1

	def __init__(self, name):
		self.name = name
		self.valvePosition = 0
		self.callBacks = []
		for i in range(self.numOutputs):
			self.callBacks.append([])
		self.reset()

	def reset(self):
		pass

	def set(self):
		pass

	def attachToSetOfNextElement(self, logicElement, outputIndex=0):
		self.attachOutputFunction(outputIndex, logicElement.set)

	def attachToReadOfNextElement(self, logicElement, outputIndex=0):
		self.attachOutputFunction(outputIndex, logicElement.pulse)

	def attachOutputFunction(self, outputIndex, function, *args):
		self.callBacks[outputIndex].append((function, args))

	def pulse(self):
		print self.name + ' got pulse'
		for i in range(self.numOutputs):
			if self.valvePosition != i:
				print 'Element {}, output {} sent pulse'.format(self.name, i)
				for callback in self.callBacks[i]:
					function, args = callback
					function(*args)


class PlusLogicElement(LogicElement):
	def reset(self):
		self.valvePosition = 0

	def set(self):
		self.valvePosition = 1


class MinusLogicElement(LogicElement):
	def reset(self):
		self.valvePosition = 1

	def set(self):
		self.valvePosition = 0


class SwitchingLogicElement(LogicElement):
	numOutputs = 2

	def reset(self):
		self.valvePosition = 1

	def set(self):
		self.valvePosition = 0


class Gate(object):
	pulsesRequired = 1

	def __init__(self, name):
		self.elements = {}
		self.inputElementNames = []
		self.outputElementName = ''
		self.outputHasFired = False
		self.callBacks = []
		self.name = name

	def setInput(self, inputIndex):
		self.elements[self.inputElementNames[inputIndex]].set()

	def reset(self):
		self.outputHasFired = False
		for k, element in self.elements.iteritems():
			element.reset()

	def pulse(self):
		pass

	def fireOutput(self):
		if not self.outputHasFired:
			print 'Gate {} has fired'.format(self.name)
			self.outputHasFired = True
			for callback in self.callBacks:
				function, args = callback
				function(*args)

	def attachOutputFunction(self, function, *args):
		self.callBacks.append((function, args))


class AndGate(Gate):
	def __init__(self, *args):
		Gate.__init__(self, args)
		self.elements['in0'] = PlusLogicElement('in0')
		self.elements['in1'] = PlusLogicElement('in1')
		self.elements['in0'].attachToReadOfNextElement(self.elements['in1'])
		self.inputElementNames = ['in0', 'in1']
		self.elements['in1'].attachOutputFunction(0, self.fireOutput)

	def pulse(self):
		self.elements['in0'].pulse()


class OrGate(Gate):
	def __init__(self, *args):
		Gate.__init__(self, args)
		self.elements['in0'] = PlusLogicElement('in0')
		self.elements['in1'] = PlusLogicElement('in1')
		self.inputElementNames = ['in0', 'in1']
		self.elements['in0'].attachOutputFunction(0, self.fireOutput)
		self.elements['in1'].attachOutputFunction(0, self.fireOutput)

	def pulse(self):
		self.elements['in0'].pulse()
		self.elements['in1'].pulse()


class XorGate(Gate):
	def __init__(self, *args):
		Gate.__init__(self, args)
		self.elements['in_A_0'] = PlusLogicElement('in_A_0')
		self.elements['in_A_1'] = MinusLogicElement('in_A_1')
		self.elements['in_B_0'] = MinusLogicElement('in_B_0')
		self.elements['in_B_1'] = PlusLogicElement('in_B_1')
		self.elements['in_A_0'].attachToReadOfNextElement(self.elements['in_A_1'])
		self.elements['in_A_1'].attachOutputFunction(0, self.fireOutput)
		self.elements['in_B_0'].attachToReadOfNextElement(self.elements['in_B_1'])
		self.elements['in_B_1'].attachOutputFunction(0, self.fireOutput)

	def setInput(self, inputIndex):
		self.elements['in_A_{}'.format(inputIndex)].set()
		self.elements['in_B_{}'.format(inputIndex)].set()

	def pulse(self):
		self.elements['in_A_0'].pulse()
		self.elements['in_B_0'].pulse()


