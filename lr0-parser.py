import sys
import termtables as tt

def get_non_terminals(productions):
	non_terminals = []
	for production in productions:
		lhs = production.split('->')[0]
		rhs = production.split('->')[1]
		for char in lhs+rhs:
			if char not in non_terminals and char.isupper():
				non_terminals.append(char)

	return non_terminals

def get_terminals(productions, non_terminals):
	terminals = []
	for production in productions:
		temp = production.split('->')[1]
		for char in temp:
			if char not in non_terminals and char not in non_terminals and char != '|':
				terminals.append(char) 

	return terminals

def find_closure(items, G):
	closure = items
	
	for item in closure:
		dot_pos = item[1].index('.')

		if (dot_pos < (len(item[1]) - 1) and item[1][dot_pos+1] in G):
			nT_next_to_dot = item[1][dot_pos+1]
			
			for production in G[nT_next_to_dot]:
				possible_item = [nT_next_to_dot, str('.') + str(production)]
				
				if (possible_item not in closure):
					closure.append(possible_item)
	
	return closure

def find_canonical_items(G, symbols, start_symbol):
	canonical_items = []
	state_transitions = []
	canonical_items.append(find_closure([['X', '.' + str(start_symbol) + '$']], G))

	for itemset in canonical_items:
		for symbol in symbols:
			if (symbol == '$'):
				continue
			
			goto = False
			shift = False
			
			intermediate = []
			
			for item in itemset:
				dot_pos = item[1].index('.')
				
				if(dot_pos < (len(item[1]) - 1) and item[1][dot_pos + 1] == symbol):
					intermediate.append([item[0], item[1][:dot_pos]+symbol + '.' + item[1][dot_pos+2:]])
				
			new_state = find_closure(intermediate, G)
			
			if(len(new_state) == 0):
				continue
			
			if(symbol in G.keys()):
				goto = True
			
			else:
				shift = True
			
			if (new_state not in canonical_items):
				if (goto):
					state_transitions.append(['GOTO',canonical_items.index(itemset)+1,len(canonical_items)+1,symbol])
				
				elif (shift):
					state_transitions.append(['SHIFT',canonical_items.index(itemset)+1,len(canonical_items)+1,symbol])
				
				canonical_items.append(new_state)

			else:
				if (goto):
					state_transitions.append(['GOTO', canonical_items.index(itemset)+1, canonical_items.index(new_state)+1, symbol])
				elif (shift):
					state_transitions.append(['SHIFT', canonical_items.index(itemset)+1, canonical_items.index(new_state)+1, symbol])

	return canonical_items, state_transitions

def make_reductions(canonical_items, G, start_symbol):
	accept_state = -1
	reductions = [ [] for i in range(len(canonical_items)) ]
	final_item = ['X', str(start_symbol)+'.$']
	final_rules = []

	# Create rules with dot on the right end for checking.
	for lhs in G.keys():
		for rhs in G[lhs]:
			final_rules.append([lhs, rhs + str('.')])

	for itemset in canonical_items:
		if (final_item in itemset):
			accept_state = canonical_items.index(itemset)+1

		for item in itemset:
			if (item in final_rules):
				reductions[canonical_items.index(itemset)].append(final_rules.index(item))

	return accept_state, reductions

def createParseTable(state_transitions, reductions, terminals, non_terminals):
	i = 0
	symbols = terminals + non_terminals
	symbolMap = dict()
	parseTable = [ ['-' for i in range(len(symbols))] for j in range(len(canonical_items)) ]

	for symbol in symbols:
		symbolMap[symbol] = i
		i = i+1

	for s in state_transitions:
		if (s[0][0] == 'S'):
			parseTable[s[1]-1][symbolMap[s[3]]] = s[0][0]+str(s[2]-1)
		else:
			parseTable[s[1]-1][symbolMap[s[3]]] = str(s[2]-1)

	parseTable[accept_state-1][symbolMap['$']] = 'Accepted'

	for i in reductions:
		if (len(i) > 0):
			for j in terminals:
				parseTable[reductions.index(i)][symbolMap[j]] = 'R' + str(i[0])

	return parseTable

def printTable():
	parseTable = createParseTable(state_transitions, reductions, terminals, non_terminals)

	table = []

	header = [''] * (len(terminals) + 1)
	header[(len(terminals) + 1) // 2] = 'Action'

	header2 = [''] * len(non_terminals)
	header2[(len(non_terminals)) // 2] = 'Goto'

	table.append([''] + terminals + non_terminals)
	for line_no, line in enumerate(parseTable):
		table.append([line_no+1] + line)

	data = [''] * (len(terminals) + len(non_terminals))

	final_table = tt.to_string(data=table, header=header + header2, style=tt.styles.ascii_thin_double, padding=(0, 1))

	print("\nParse Table:")
	print(final_table)
	print("\n")

productions = []
start_symbol = ''

# Reading grammar from file.


try:
	with open('./' + sys.argv[1], 'r') as file:
		for line in file.readlines():
			if (len(line) == 2):
				start_symbol = line[0]
				continue
			productions.append(line.strip().replace('\n', ''))

except FileNotFoundError:
	print('\n' + sys.argv[1] + ' does not exist!\n')
	exit()

print('\nGrammar:')
print(productions)

non_terminals = get_non_terminals(productions)
terminals = get_terminals(productions, non_terminals)
print('\nTerminals & Non-Terminals:')
print(terminals)
print(non_terminals)

G = dict()
terminals += '$'
symbols = terminals + non_terminals

for production in productions:
	lhs = production.split('->')[0]
	rhs = production.split('->')[1].split('|')
	G[lhs] = rhs

canonical_items, state_transitions = find_canonical_items(G, symbols, start_symbol)

print('\nCanonical Items:')
for line_no, line in enumerate(canonical_items):
	print(str(line_no+1) + '\t', line)

print('\nState Transitions:')
for line_no, line in enumerate(state_transitions):
	print(str(line_no+1) + '\t', line)

accept_state, reductions = make_reductions(canonical_items, G, start_symbol)

printTable()