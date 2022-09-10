import graph_parsing_components as GPC
from re_parser import re_line_parser, re_rule_set
from graph import node_set, node_place_holder

class generic_parser(re_line_parser):

	@classmethod
	def parse_text(cls, text):
		for line in text.split('\n'):
			if match := cls.match_line(cls.rules, line):
				yield match
			elif clean_line := line.strip():
				yield GPC.unparsed(clean_line)



class graph_parser(generic_parser):
	rules = re_rule_set()

	@rules.handle_pattern(r'\s*#(.*)')
	def comment(match, cmt):
		return GPC.comment(cmt)


	@rules.handle_pattern(r'\s*alias:\s*(?P<alias_name>\S+)\s+(?P<target>\S+)\s*')
	def define_alias(match, alias_name, target):
		return GPC.alias(alias_name, target)

	@rules.handle_pattern(r'\s*collection:\s*(?P<collection_name>\S+)\s+(?P<target_list>.*)')
	def define_collection(match, collection_name, target_list):
		return GPC.collection(collection_name, target_list)

	@rules.handle_pattern(r'\s*implicit:\s*([\d.]+)\s*:\s*(?P<condition>.*?)→(?P<products>.*)')
	def define_implicit_rule(match, weight, condition, products):
		return GPC.implicit_rule(float(weight), condition, products.split('→'))


	@rules.handle_pattern(r'\s*([\d.]+):\s*(.*)')
	def define_weight(match, weight, line):
		return GPC.weighted_line(float(weight), line)


	@rules.handle_pattern(r'\s*(\S+):\s*(.*)')
	def unknown_command(match, cmd, line):
		raise Exception(f'Unknown command: {cmd!r} (line={line!r})')



def apply_definition(target, definition, initial_alias_table=None):

	alias_table = dict(initial_alias_table) if initial_alias_table else dict()

	def get_node(name):	#TODO - return node and not string
		candidate = alias_table.get(name, name)

		if isinstance(candidate, str):
			return target.get_or_create_node(candidate)
		else:
			return candidate


	def parse_line(line, weight=1.0):
		# subject relation object = S R O

		# The read pattern is
		# S1 R1 O1/S2 R2 O2/S3 R3 O3

		PS, PR, PO = None, None, None

		for word in line.split():
			if PS is None:
				PS = get_node(word)
			elif PR is None:
				PR = get_node(word)
			else:
				PO = get_node(word)
				target.associate(PS, PR, PO, weight)

				PS, PR, PO = PO, None, None

		#TODO - we should make sure we don't end with a PR set


	def parse_line_2(refs, line):
		#TODO - better name
		# subject relation object = S R O

		# The read pattern is
		# S1 R1 O1/S2 R2 O2/S3 R3 O3

		def get_ref(name):
			if name.isupper():
				if existing := refs.get(name):
					return existing
				else:
					refs[name] = new_ref = node_place_holder(name)
					return new_ref
			else:
				return get_node(name)

		PS, PR, PO = None, None, None

		for word in line.split():
			if PS is None:
				PS = get_ref(word)
			elif PR is None:
				PR = get_ref(word)
			else:
				PO = get_ref(word)
				yield (PS, PR, PO)

				PS, PR, PO = PO, None, None

		#TODO - we should make sure we don't end with a PR set



	for item in graph_parser.parse_text(definition):

		if isinstance(item, GPC.alias):
			alias_table[item.alias] = item.target

		elif isinstance(item, GPC.weighted_line):
			parse_line(item.line, item.weight)

		elif isinstance(item, GPC.collection):
			alias_table[item.name] = node_set(get_node(target) for target in item.target_list.split())


		elif isinstance(item, GPC.implicit_rule):
			refs = dict()
			target.create_implicit_rule(item.weight, tuple(parse_line_2(refs, item.condition)), *(tuple(parse_line_2(refs, p)) for p in item.products))



		elif isinstance(item, GPC.comment):
			pass

		elif isinstance(item, GPC.unparsed):
			parse_line(item.text)



		else:
			raise Exception(item)




