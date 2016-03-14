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


class LogicBlock(object):
	pulsesRequired = 1

	def __init__(self, name):
		self.elements = {}
		self.outputHasFired = False
		self.callBacks = []
		self.name = name

	def setInput(self, inputName):
		self.elements[inputName].set()

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


class AndGate(LogicBlock):
	def __init__(self, *args):
		LogicBlock.__init__(self, args)
		self.elements['A'] = PlusLogicElement('A')
		self.elements['B'] = PlusLogicElement('B')
		self.elements['A'].attachToReadOfNextElement(self.elements['B'])
		self.elements['B'].attachOutputFunction(0, self.fireOutput)

	def pulse(self):
		self.elements['A'].pulse()


class OrGate(LogicBlock):
	def __init__(self, *args):
		LogicBlock.__init__(self, args)
		self.elements['A'] = PlusLogicElement('A')
		self.elements['B'] = PlusLogicElement('B')
		self.elements['A'].attachOutputFunction(0, self.fireOutput)
		self.elements['B'].attachOutputFunction(0, self.fireOutput)

	def pulse(self):
		self.elements['A'].pulse()
		self.elements['B'].pulse()


class XorGate(LogicBlock):
	def __init__(self, *args):
		LogicBlock.__init__(self, args)
		self.elements['A_0'] = PlusLogicElement('A_0')
		self.elements['B_0'] = MinusLogicElement('B_0')
		self.elements['A_1'] = MinusLogicElement('A_1')
		self.elements['B_1'] = PlusLogicElement('B_1')
		self.elements['A_0'].attachToReadOfNextElement(self.elements['B_0'])
		self.elements['B_0'].attachOutputFunction(0, self.fireOutput)
		self.elements['A_1'].attachToReadOfNextElement(self.elements['B_1'])
		self.elements['B_1'].attachOutputFunction(0, self.fireOutput)

	def setInput(self, inputName):
		self.elements['{}_0'.format(inputName)].set()
		self.elements['{}_1'.format(inputName)].set()

	def pulse(self):
		self.elements['A_0'].pulse()
		self.elements['A_1'].pulse()


class HalfAdder(LogicBlock):
	def __init__(self, *args):
		LogicBlock.__init__(self, args)
		self.elements['xor'] = XorGate('xor')
		self.elements['and'] = AndGate('and')
		self.elements['xor'].attachOutputFunction(0, self.fireOutput, 'sum')
		self.elements['and'].attachOutputFunction(0, self.fireOutput, 'carry')
		self.callBacks = {'sum': [], 'carry': []}
		self.outputHasFired = {'sum': False, 'carry': False}

	def setInput(self, inputName):
		self.elements['xor'].setInput(inputName)
		self.elements['and'].setInput(inputName)

	def pulse(self):
		self.elements['xor'].pulse()
		self.elements['and'].pulse()

	def fireOutput(self, outputName):
		if not self.outputHasFired[outputName]:
			print 'Block {}, output {} has fired'.format(self.name, outputName)
			self.outputHasFired[outputName] = True
			for callback in self.callBacks[outputName]:
				function, args = callback
				function(*args)



