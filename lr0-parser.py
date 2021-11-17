def get_terminals(productions):
	terminals = []
	for production in productions:
		if production[0] not in terminals and production[0].isupper():
			terminals.append(production[0]) 

	return terminals

def get_non_terminals(productions):
	non_terminals = []
	for production in productions:
		temp = production.split('->')
		for char in temp[1]:
			if char not in non_terminals and char.islower():
				non_terminals.append(char) 

	return non_terminals

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

def find_canonical_items(G, symbols):
	canonical_items = []
	state_transitions = []
	canonical_items.append(find_closure([['X', '.S$']], G))

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
					state_transitions.append(['g',canonical_items.index(itemset)+1,len(canonical_items)+1,symbol])
				
				elif (shift):
					state_transitions.append(['s',canonical_items.index(itemset)+1,len(canonical_items)+1,symbol])
				
				canonical_items.append(new_state)

			else:
				if (goto):
					state_transitions.append(['g', canonical_items.index(itemset)+1, canonical_items.index(new_state)+1, symbol])
				elif (shift):
					state_transitions.append(['s', canonical_items.index(itemset)+1, canonical_items.index(new_state)+1, symbol])

	return canonical_items, state_transitions

productions = ['S->AA', 'A->aA|b']

print('Grammar:')
print(productions)

terminals = get_terminals(productions)
non_terminals = get_non_terminals(productions)
symbols = terminals + non_terminals
print('\nTerminals & Non-Terminals:')
print(terminals)
print(non_terminals)
print(symbols)

G = dict()
terminals += '$'

for production in productions:
	lhs = production.split('->')[0]
	rhs = production.split('->')[1].split('|')
	G[lhs] = rhs

canonical_items, state_transitions = find_canonical_items(G, symbols)

print(canonical_items)

print(state_transitions)