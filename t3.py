from graph import graph
from graph_parser import apply_definition

#notation - upper case is place holder

graph_def = '''

	alias: > is-harder-than
	diamond > stone > gold > wax > water
	0.25: here is-example fuzzy


	#Note - create a collection that has the one member > in it
	# The reason to use collections for this (or later classifiers) is so that we know when to invoke a certain rule
	collection: ⌬ >

	# This rule is only useful for scalar comparison, which we unorthodoxely symbolize with a benzene ring
	implicit: 0.75: A ⌬ B ⌬ C → A ⌬ C

	#implicit: 0.5: A is-example fuzzy → A is-fuzzy yes → A is-so-fluffy yes

'''

G = graph()
apply_definition(G, graph_def)

for (S, R, O), W in G._connections.items():
	print(f'{S.name} - {R.name} - {O.name} : {W}')


GN = G.get_or_create_node




print('\n-- QUERY --\n')
for (S, R, O), W in G.query_connections(GN('here')):
	print(f'{S.name} - {R.name} - {O.name} : {W}')

print('\n-- QUERY IMPL CON --\n')

for (S, R, O), W in G.query_implicit_connections(relation=GN('is-harder-than')):
	print(f'{S.name} - {R.name} - {O.name} : {W}')




# diamond - is-harder-than - stone : 1.0
# stone - is-harder-than - gold : 1.0
# gold - is-harder-than - wax : 1.0
# wax - is-harder-than - water : 1.0
# here - is-example - fuzzy : 0.25


#Next step is to apply implicit listings of connections based on a rule set

# The rule will use → to define the target from the source but these things may be complex graphs. Maybe they can't be explained on a single line unless we can also create macros
