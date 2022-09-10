from collections import defaultdict, deque

class node:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f'<{self.__class__.__qualname__} `{self.name}´>'


class captured_node:
	def __init__(self, condition, target):
		self.condition = condition
		self.target = target

	def __repr__(self):
		return f'<{self.__class__.__qualname__} {self.condition} → `{self.target.name}´>'

class node_place_holder:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f'<{self.__class__.__qualname__} `{self.name}´>'

class node_set:
	def __init__(self, nodes):
		self._nodes = set(nodes)

	def __contains__(self, item):
		return item in self._nodes

	def __repr__(self):
		return f'<{self.__class__.__qualname__} with {len(self._nodes)} nodes>'

class implicit_rule:
	def __init__(self, weight, condition, product_list):
		self.weight = weight
		self.condition = condition
		self.product_list = product_list

	def __repr__(self):
		return f'<{self.__class__.__qualname__} with {len(self.product_list)} products, weight={self.weight!r}>'


class implicit_rule_condition:
	def __init__(self, condition):
		self.condition = condition

	def __repr__(self):
		return f'<{self.__class__.__qualname__}>'



	def match(self, state, subject, relation, object):
		#print('STATE', state)
		pending_state = dict()
		S, R, O = subject, relation, object

		def node_match(item, condition):
			if isinstance(condition, node):
				if item is condition:
					return item
			elif isinstance(condition, node_place_holder):

				if already_captured := state.get(condition):


					if item is already_captured.target:
						#print('ALREADY CAPT!', already_captured, '\t', item)
						return already_captured

				else:

					captured = pending_state[condition] = captured_node(condition, item)
					return captured


			elif isinstance(condition, node_set):

				if already_captured := state.get(condition):
					if item is already_captured.target:
						#print('ALREADY CAPT!', already_captured, '\t', item)
						return already_captured

				elif item in condition:
					captured = pending_state[condition] = captured_node(condition, item)
					return captured
			else:
				raise Exception(condition)



		CS, CR, CO = self.condition

		MS = node_match(S, CS)
		MR = node_match(R, CR)
		MO = node_match(O, CO)

		if MS and MR and MO:
			#If this is a match we update state with the pending state
			state.update(pending_state)
			return MS, MR, MO


class implicit_rule_product:
	def __init__(self, product):
		self.product = product

	def iter_product_connections(self, state):
		def get_node(item):
			if isinstance(item, node_place_holder):
				return get_node(state[item])
			elif isinstance(item, node_set):	#Use node_set as place holder as well
				return get_node(state[item])
			elif isinstance(item, captured_node):
				return item.target
			else:
				raise Exception(item)

		for connection in self.product:
			yield tuple(get_node(n) for n in connection)



	def __repr__(self):
		return f'<{self.__class__.__qualname__}>'

class graph:
	def __init__(self, name=None):
		self.name = name or 'anonymous'
		self._connections = defaultdict(float)
		self._nodes = dict()
		self._implicit_rules = deque()

	def create_implicit_rule(self, weight, condition, *products):
		self._implicit_rules.append(implicit_rule(weight, tuple(implicit_rule_condition(sub_condition) for sub_condition in condition), tuple(implicit_rule_product(p) for p in products)))

	def create_nodes(self, *node_names):
		for name in node_names:
			yield self.get_or_create_node(name)

	def get_or_create_node(self, name):

		if existing_node := self._nodes.get(name):
			return existing_node
		else:
			new_node = node(name)
			self._nodes[name] = new_node
			return new_node


	def query_connections(self, subject=None, relation=None, object=None):
		TS, TR, TO = subject, relation, object

		for (S, R, O), value in self._connections.items():

			MS = TS is None or TS is S
			MR = TR is None or TR is R
			MO = TO is None or TO is O

			if MS and MR and MO:
				yield (S, R, O), value


	def query_implicit_connections(self, subject=None, relation=None, object=None, connections_to_check=None):

		if connections_to_check is None:
			connections_to_check = self._connections.items()

		for (S, R, O), W in self.query_connections(subject, relation, object):
			#print('===============')
			#print(S, R, O, W)
			#print('===============')
			for rule in self._implicit_rules:

				local_state = dict()

				first_condition, *remaining = rule.condition
				match = first_condition.match(local_state, S, R, O)

				#print(first_condition.condition)
				#print('FIRST', match)

				for condition in remaining:
					if not match:
						break


					#print('COND', condition.condition)
					match = None
					for (S2, R2, O2), W2 in connections_to_check:
						if sub_match := condition.match(local_state, S2, R2, O2):
							#print('S2, R2, O2', S2, R2, O2)
							#print('SUBMATCH', sub_match)
							match = sub_match
							break	#Should we stop searching here?


					if match:
						#print('CONDITIONAL CHAIN MATCH!')
						#print(local_state)
						for p in rule.product_list:
							for product_connection in p.iter_product_connections(local_state):
								yield product_connection, W * W2 * rule.weight



	def __repr__(self):
		return f'<{self.__class__.__qualname__} `{self.name}´ with {len(self._nodes)} nodes and {len(self._connections)} connections>'

	def associate(self, subject, relation, object, value=1.0):
		self._connections[(subject, relation, object)] += value

	def calculate_direct_match(self, subject, relation, object):

		TS, TR, TO = subject, relation, object

		points = 0
		for (S, R, O), value in self._connections.items():

			if S is TS and R is TR and O is TO:
				points += 1.0

			elif S is TS and R is TR:
				points += 0.5

			elif O is TO and R is TR:
				points += 0.5

			elif S is TS:
				points += 0.1

			elif O is TO:
				points += 0.1

			elif R is TR:
				points += 0.1


		return points
