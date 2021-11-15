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

# def closure()

# def goto()

# def generate_automaton(productions):

# def generate_table(states)

productions = ['S->AA', 'A->aA', 'A->b']

print('Grammer:')
print(productions)

terminals = get_terminals(productions)
non_terminals = get_non_terminals(productions)

print('\nTerminals & Non-Terminals:')
print(terminals)
print(non_terminals)

augment(productions)
print('\nAugmented Grammar:')
print(productions)

append_dot(productions)

# states = generate_automaton(productions)
# table = generate_table(states)

# Print table.