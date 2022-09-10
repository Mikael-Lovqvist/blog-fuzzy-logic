
class alias:
	def __init__(self, alias, target):
		self.alias = alias
		self.target = target

	def __repr__(self):
		return f'<{self.__class__.__qualname__} alias={self.alias!r} target={self.target!r}>'

class collection:
	def __init__(self, name, target_list):
		self.name = name
		self.target_list = target_list

	def __repr__(self):
		return f'<{self.__class__.__qualname__} name={self.name!r} target_list={self.target_list!r}>'

class weighted_line:
	def __init__(self, weight, line):
		self.weight = weight
		self.line = line

	def __repr__(self):
		return f'<{self.__class__.__qualname__} weight={self.weight!r} line={self.line!r}>'

class implicit_rule:
	def __init__(self, weight, condition, products):
		self.weight = weight
		self.condition = condition
		self.products = products

	def __repr__(self):
		return f'<{self.__class__.__qualname__} weight={self.weight!r} condition={self.condition!r} products={self.products!r}>'

class unparsed:
	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return f'<{self.__class__.__qualname__} {self.text!r}>'

class comment:
	def __init__(self, text):
		self.text = text

	def __repr__(self):
		return f'<{self.__class__.__qualname__} {self.text!r}>'

