class LogicElement(object):
	def __init__(self, name):
		self.valveBlocksExit = None
		self.reset()
		self.callBacks = []
		self.name = name

	def reset(self):
		pass

	def set(self):
		pass

	def read(self):
		return not self.valveBlocksExit

	def attachToSetOfNextElement(self, logicElement):
		self.attachOutputFunction(logicElement.set)

	def attachToReadOfNextElement(self, logicElement):
		self.attachOutputFunction(logicElement.pulse)

	def attachOutputFunction(self, function, *args):
		self.callBacks.append((function, args))

	def pulse(self):
		print self.name + ' got pulse'
		if not self.valveBlocksExit:
			print self.name + ' sent pulse'
			for callback in self.callBacks:
				function, args = callback
				function(*args)


class PlusLogicElement(LogicElement):
	def reset(self):
		self.valveBlocksExit = True

	def set(self):
		self.valveBlocksExit = False


class MinusLogicElement(LogicElement):
	def reset(self):
		self.valveBlocksExit = False

	def set(self):
		self.valveBlocksExit = True


class Gate(object):
	def __init__(self):
		self.pulsesRequired = 0
		self.elements = {}
		self.inputElementNames = []
		self.outputElementName = ''

	def setInput(self, inputIndex):
		self.elements[self.inputElementNames[inputIndex]].set()

	def read(self):
		return self.elements[self.outputElementName].read()

	def reset(self):
		for k, element in self.elements.iteritems():
			element.reset()

	def pulse(self):
		pass


class AndGate(Gate):
	def __init__(self):
		Gate.__init__(self)
		self.elements['in0'] = PlusLogicElement('in0')
		self.elements['in1'] = PlusLogicElement('in1')
		self.elements['in0'].attachToReadOfNextElement(self.elements['in1'])
		self.pulsesRequired = 2
		self.inputElementNames = ['in0', 'in1']
		self.outputElementName = 'in1'
		self.elements['in1'].attachOutputFunction(printIsStupid, 'Gate output fired')

	def pulse(self):
		self.elements['in0'].pulse()


def printIsStupid(val):
	print val