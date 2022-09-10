from graph import graph
from graph_parser import apply_definition

#Cleaned up example - only focusing on the implicit rule

#notation - upper case is place holder

graph_def = '''

	alias: > is-harder-than
	diamond > stone > gold > wax > water

	# Create a collection represented by a benzene ring - it only contains the is-harder-than relation for now
	collection: ⌬ >

	# Define rule for implicit deduction
	implicit: 0.75: A ⌬ B ⌬ C → A ⌬ C

'''

G = graph()
apply_definition(G, graph_def)

for (S, R, O), W in G._connections.items():
	print(f'{S.name} - {R.name} - {O.name} : {W}')


GN = G.get_or_create_node

print('\n-- QUERY 1 --\n')

result_1 = tuple(G.query_implicit_connections(relation=GN('is-harder-than')))
for (S, R, O), W in result_1:
	print(f'{S.name} - {R.name} - {O.name} : {W}')

print('\n-- QUERY 2 --\n')
result_2 = tuple(G.query_implicit_connections(relation=GN('is-harder-than'), connections_to_check=result_1))
for (S, R, O), W in result_2:
	print(f'{S.name} - {R.name} - {O.name} : {W}')

print('\n-- QUERY 3 --\n')
result_3 = tuple(G.query_implicit_connections(relation=GN('is-harder-than'), connections_to_check=result_2))
for (S, R, O), W in result_3:
	print(f'{S.name} - {R.name} - {O.name} : {W}')

