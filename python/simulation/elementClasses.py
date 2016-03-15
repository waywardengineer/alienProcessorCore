class LogicElement(object):
	def __init__(self, name):
		self.name = name
		self.callBacks = {'out': []}
		self.outputsHaveTriggered = {'out': False}

	def reset(self):
		for outputName in self.outputsHaveTriggered:
			self.outputsHaveTriggered[outputName] = False

	def attachOutputFunction(self, outputName, function, *args):
		self.callBacks[outputName].append((function, args))

	def fireRead(self):
		pass

	def triggerOutput(self, outputName='out'):
		if not self.outputsHaveTriggered[outputName]:
			print 'Block {}, output {} has fired'.format(self.name, outputName)
			self.outputsHaveTriggered[outputName] = True
			for callback in self.callBacks[outputName]:
				function, args = callback
				function(*args)


class PhysicalBaseElement(LogicElement):
	def __init__(self, *args):
		LogicElement.__init__(self, *args)
		self.valvePosition = 0
		self.reset()

	def set(self):
		pass

	def attachToSetOfNextElement(self, logicElement):
		self.attachOutputFunction('out', logicElement.set)

	def attachToReadOfNextElement(self, logicElement):
		self.attachOutputFunction('out', logicElement.fireRead)

	def fireRead(self):
		if not self.valvePosition == 0:
			self.triggerOutput()


class PlusLogicElement(PhysicalBaseElement):
	def reset(self):
		LogicElement.reset(self)
		self.valvePosition = 0

	def set(self):
		self.valvePosition = 1


class MinusLogicElement(PhysicalBaseElement):
	def reset(self):
		LogicElement.reset(self)
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
		self.elements['A'].attachOutputFunction('out', self.elements['B'].fireRead)
		self.elements['B'].attachOutputFunction('out', self.triggerOutput)

	def fireRead(self):
		self.elements['A'].fireRead()


class OrGate(LogicBlock):
	def __init__(self, *args):
		LogicBlock.__init__(self, *args)
		self.elements['A'] = PlusLogicElement('A')
		self.elements['B'] = PlusLogicElement('B')
		self.elements['A'].attachOutputFunction('out', self.triggerOutput)
		self.elements['B'].attachOutputFunction('out', self.triggerOutput)

	def fireRead(self):
		self.elements['A'].fireRead()
		self.elements['B'].fireRead()


class XorGate(LogicBlock):
	def __init__(self, *args):
		LogicBlock.__init__(self, *args)
		self.elements['A_0'] = PlusLogicElement('A_0')
		self.elements['B_0'] = MinusLogicElement('B_0')
		self.elements['A_1'] = MinusLogicElement('A_1')
		self.elements['B_1'] = PlusLogicElement('B_1')
		self.elements['A_0'].attachToReadOfNextElement(self.elements['B_0'])
		self.elements['B_0'].attachOutputFunction('out', self.triggerOutput)
		self.elements['A_1'].attachToReadOfNextElement(self.elements['B_1'])
		self.elements['B_1'].attachOutputFunction('out', self.triggerOutput)

	def setInput(self, inputName):
		self.elements['{}_0'.format(inputName)].set()
		self.elements['{}_1'.format(inputName)].set()

	def fireRead(self):
		self.elements['A_0'].fireRead()
		self.elements['A_1'].fireRead()


class HalfAdder(LogicBlock):
	def __init__(self, *args):
		LogicBlock.__init__(self, args)
		self.callBacks = {'sum': [], 'carry': []}
		self.outputsHaveTriggered = {'sum': False, 'carry': False}
		self.elements['xor'] = XorGate('xor')
		self.elements['and'] = AndGate('and')
		self.elements['xor'].attachOutputFunction('out', self.triggerOutput, 'sum')
		self.elements['and'].attachOutputFunction('out', self.triggerOutput, 'carry')

	def setInput(self, inputName):
		self.elements['xor'].setInput(inputName)
		self.elements['and'].setInput(inputName)

	def fireRead(self):
		self.elements['xor'].fireRead()
		self.elements['and'].fireRead()




