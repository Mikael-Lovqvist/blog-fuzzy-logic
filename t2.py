from collections import defaultdict

DEFAULT_LIMIT = 1e-15

class node:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f'<{self.__class__.__qualname__} `{self.name}´>'


class graph:
	def __init__(self, name=None):
		self.name = name or 'anonymous'
		self._connections = defaultdict(float)
		self._nodes = set()

	def create_nodes(self, *node_names):
		for name in node_names:
			new_node = node(name)
			self._nodes.add(new_node)
			yield new_node

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

G = graph()

bread, butter, cheese, condiment_for = G.create_nodes('bread', 'butter', 'cheese', 'condiment_for')
fluffy, hardness_at_room_conditions_like, stone, water, harder_than, softer_than = G.create_nodes(*'fluffy hardness_at_room_conditions_like stone water harder_than softer_than'.split())

harder_than_water, softer_than_stone = G.create_nodes(*'harder_than_water harder_than_water'.split())
sponge, rock, homogenicity, homogenous = G.create_nodes(*'sponge rock homogenicity homogenous'.split())


G.associate(harder_than_water, harder_than, water)
G.associate(softer_than_stone, softer_than, stone)

#Setup comparisons between butter, bread and sponge, they are all harder than water and softer than stone
G.associate(butter, hardness_at_room_conditions_like, softer_than_stone)
G.associate(butter, hardness_at_room_conditions_like, harder_than_water)

G.associate(bread, hardness_at_room_conditions_like, softer_than_stone)
G.associate(bread, hardness_at_room_conditions_like, harder_than_water)

G.associate(sponge, hardness_at_room_conditions_like, harder_than_water)
G.associate(sponge, hardness_at_room_conditions_like, softer_than_stone)

#Setup comparisons between butter, bread and sponge relating to fluffyness

G.associate(bread, homogenicity, fluffy)
G.associate(sponge, homogenicity, fluffy)
G.associate(butter, homogenicity, homogenous)

G.associate(butter, condiment_for, bread)



comp = homogenicity
print('G.calculate_direct_match(bread, comp, butter)',  G.calculate_direct_match(bread, comp, butter))
print('G.calculate_direct_match(bread, comp, sponge)',  G.calculate_direct_match(bread, comp, sponge))
print('G.calculate_direct_match(butter, comp, sponge)',  G.calculate_direct_match(butter, comp, sponge))
print('G.calculate_direct_match(bread, comp, stone)',  G.calculate_direct_match(bread, comp, stone))
print('G.calculate_direct_match(bread, comp, water)',  G.calculate_direct_match(bread, comp, water))

