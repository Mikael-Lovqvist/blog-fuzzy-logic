from collections import defaultdict

#note - this model is completely wrong. Let's redo in t2


DEFAULT_LIMIT = 1e-15


class association:
	def __init__(self):
		self._map = defaultdict(float)

	def prune(self, limit=DEFAULT_LIMIT):
		to_prune = {k for k, v in self._map.items() if abs(v) <= limit}
		for item in to_prune:
			self._map.pop(item, None)

	def __len__(self):
		return len(self._map)

	def associate(self, target, value):
		self._map[target] += value

class association_map:
	def __init__(self):
		self._as_source = association()
		self._as_destination = association()

	def prune(self, limit=DEFAULT_LIMIT):
		self._as_source.prune(limit)
		self._as_destination.prune(limit)

	def __len__(self):
		return len(self._as_source) + len(self._as_destination)


	def associate(self, source, destination, value):
		#tbd - should we mess with destinations private stuff?
		self._as_source.associate(destination, value)
		destination._associations._as_destination.associate(source, value)


class node:
	def __init__(self, name):
		self.name = name
		self._associations = association_map()

	def prune(self, limit=DEFAULT_LIMIT):
		self._associations.prune(limit)

	def __len__(self):
		return len(self._associations)

	def __repr__(self):
		return f'<{self.__class__.__qualname__} `{self.name}´ with {len(self._associations)} associations>'


	def associate_with(self, target, value):
		self._associations.associate(self, target, value)

class node_collection:
	def __init__(self):
		self._nodes = set()

	def prune(self, limit=DEFAULT_LIMIT):
		for node in self._nodes:
			node.prune(limit)

	def __len__(self):
		return len(self._nodes)

	def __repr__(self):
		return f'<{self.__class__.__qualname__} with {len(self._nodes)} nodes>'

	def add(self, *node_list):
		for node in node_list:
			self._nodes.add(node)

class graph:
	def __init__(self, name=None):
		self.name = name or 'anonymous'
		self._nodes = node_collection()

	def prune(self, limit=DEFAULT_LIMIT):
		self._nodes.prune(limit)

	def add_node(self, *node_list):
		self._nodes.add(*node_list)

	def __repr__(self):
		return f'<{self.__class__.__qualname__} `{self.name}´ with {len(self._nodes)} nodes>'

G = graph()

bread = node('bread')
butter = node('butter')

G.add_node(bread, butter)

