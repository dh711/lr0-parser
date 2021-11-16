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

def augment(productions):
	productions.insert(0, 'X->S')

def append_dot(productions):
	for production in productions:
		production.replace('->', '->.')

def find_closure(item):
	c = [item]
	for item in c:
		dot_pos = item.index('.')
		if dot_pos != len(item)-1:
			target = dot_pos + 1
			for production in productions:
				if production[0] == item[target] and append_dot(production) not in c:
					c.append(append_dot(production))

	return c

def goto(item):
	temp = []
	dot_pos = item.index('.')
	if dot_pos < len(item)-1:
		new_item = item[0:dot_pos] + item[dot_pos+1] + '.' + item[dot_pos+2:]
		if new_item.index('.') == len(new_item) - 1:
			temp.append(new_item)
			return temp
		else:
			c = find_closure(new_item)
			return c
	else:
		return item

def find_next_states(states, symbols):
	pass

# def generate_table(states)

productions = ['S->AA', 'A->aA', 'A->b']

print('Grammar:')
print(productions)

terminals = get_terminals(productions)
non_terminals = get_non_terminals(productions)
symbols = terminals + non_terminals

print('\nTerminals & Non-Terminals:')
print(terminals)
print(non_terminals)
print(symbols)

augment(productions)
print('\nAugmented Grammar:')
print(productions)

append_dot(productions)

# states = [[1, productions]]
# find_next_states(states)
# print('\nStates:')
# print(states)


# table = generate_table(states)

# Print table.