import re
from collections import deque

class pending_re_rule:
	def __init__(self, rule_set, pattern, flags=0):
		self.rule_set = rule_set
		self.pattern = re.compile(pattern, flags)

	def __call__(self, function):
		return self.rule_set.register_re_rule(self.pattern, function)

class re_match:
	def __init__(self, rule_set, rule, match):
		self.rule_set = rule_set
		self.rule = rule
		self.match = match

	def get_arguments(self):
		return self.rule.get_arguments_from_match(self.match)

class re_rule:
	def __init__(self, pattern, function):
		self.pattern = pattern
		self.function = function
		self.index_map = {index: name for name, index in pattern.groupindex.items()}

	def match_line(self, line):
		return self.pattern.match(line)


	def get_arguments_from_match(self, match):
		named, positional = dict(), deque()
		for index, value in enumerate(match.groups(), 1):
			if name := self.index_map.get(index):
				named[name] = value
			else:
				positional.append(value)

		return positional, named

class re_rule_set:
	def __init__(self):
		self.rules = deque()
		self.name = None
		self.target = None

	def __set_name__(self, target, name):
		self.target, self.name = target, name


	def register_re_rule(self, pattern, function):
		new_rule = re_rule(pattern, function)
		self.rules.append(new_rule)
		return new_rule

	def handle_pattern(self, pattern, flags=0):
		return pending_re_rule(self, pattern, flags)

	def match_line(self, line):
		for rule in self.rules:
			if match := rule.match_line(line):
				return re_match(self, rule, match)

class re_line_parser:

	@staticmethod
	def match_line(rules, line):
		if match := rules.match_line(line):
			positional, named = match.get_arguments()
			return match.rule.function(match, *positional, **named)
