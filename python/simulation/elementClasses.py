class LogicElement(object):
	def __init__(self, name):
		self.name = name
		self.callBacks = {'out': []}
		self.outputsHaveFired = {'out': False}

	def reset(self):
		for outputName in self.outputsHaveFired:
			self.outputsHaveFired[outputName] = False

	def set(self):
		pass

	def attachOutputFunction(self, outputName, function, *args):
		self.callBacks[outputName].append((function, args))

	def pulse(self):
		pass

	def fireOutput(self, outputName='out'):
		if not self.outputsHaveFired[outputName]:
			print 'Block {}, output {} has fired'.format(self.name, outputName)
			self.outputsHaveFired[outputName] = True
			for callback in self.callBacks[outputName]:
				function, args = callback
				function(*args)


class PhysicalBaseElement(LogicElement):
	def __init__(self, *args):
		LogicElement.__init__(self, *args)
		self.valvePosition = 0
		self.reset()

	def attachToSetOfNextElement(self, logicElement):
		self.attachOutputFunction('out', logicElement.set)

	def attachToReadOfNextElement(self, logicElement):
		self.attachOutputFunction('out', logicElement.pulse)

	def pulse(self):
		self.fireOutput()

	def fireOutput(self, outputName='out'):
		if not self.valvePosition == 0:
			LogicElement.fireOutput(self, outputName)


class PlusLogicElement(PhysicalBaseElement):
	def reset(self):
		self.valvePosition = 0

	def set(self):
		self.valvePosition = 1


class MinusLogicElement(PhysicalBaseElement):
	def reset(self):
		self.valvePosition = 1

	def set(self):
		self.valvePosition = 0


class LogicBlock(LogicElement):

	def __init__(self, *args):
		LogicElement.__init__(self, *args)
		self.elements = {}

	def setInput(self, inputName):
		self.elements[inputName].set()

	def reset(self):
		LogicElement.reset(self)
		for k, element in self.elements.iteritems():
			element.reset()


class AndGate(LogicBlock):
	def __init__(self, *args):
		LogicBlock.__init__(self, *args)
		self.elements['A'] = PlusLogicElement('A')
		self.elements['B'] = PlusLogicElement('B')
		self.elements['A'].attachOutputFunction('out', self.elements['B'].pulse)
		self.elements['B'].attachOutputFunction('out', self.fireOutput)

	def pulse(self):
		self.elements['A'].pulse()


class OrGate(LogicBlock):
	def __init__(self, *args):
		LogicBlock.__init__(self, args)
		self.elements['A'] = PlusLogicElement('A')
		self.elements['B'] = PlusLogicElement('B')
		self.elements['A'].attachOutputFunction('out', self.fireOutput)
		self.elements['B'].attachOutputFunction('out', self.fireOutput)

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
		self.elements['B_0'].attachOutputFunction('out', self.fireOutput)
		self.elements['A_1'].attachToReadOfNextElement(self.elements['B_1'])
		self.elements['B_1'].attachOutputFunction('out', self.fireOutput)

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
		self.elements['xor'].attachOutputFunction('sum', self.fireOutput)
		self.elements['and'].attachOutputFunction('carry', self.fireOutput)
		self.callBacks = {'sum': [], 'carry': []}
		self.outputHasFired = {'sum': False, 'carry': False}

	def setInput(self, inputName):
		self.elements['xor'].setInput(inputName)
		self.elements['and'].setInput(inputName)

	def pulse(self):
		self.elements['xor'].pulse()
		self.elements['and'].pulse()




