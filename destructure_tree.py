def match_type(v_type: str):
	match v_type:
		case "INTEGER":
			return "int"
		case "REAL":
			return "float"
		case "STRING" | "CHAR":
			return "str"
		case "BOOLEAN":
			return "bool"
		case "DATE":
			raise Exception("WIP!")

def match_operator(tree: tuple, recursion_count: int, operators: list):
	op = tree[0]
	#if recursion_count > 0:
	#	recursion_count -= 1
	match op:
		case "DECLARE":
			tail = " = "
			match tree[1][1]:
				case "INTEGER":
					tail += "0"
				case "REAL":
					tail += "0.0"
				case "STRING" | "CHAR":
					tail += "''"
				case "BOOLEAN":
					tail += "false"
				case "DATE":
					#tail += "datetime.datetime.new()"
					raise Exception("WIP!")
			return "  " * recursion_count + destructure_tree(tree[1][0], recursion_count + 1, operators) + tail + "\n"

		case "<-":
			return "  " * recursion_count + tree[1][0] + " = " + destructure_tree(tree[1][1], recursion_count + 1, operators) + "\n"
		
		case "<" | ">" | ">=" | "<=" | "+" | "-" | "*" | "/":
			return "(float(" + destructure_tree(tree[1][0], recursion_count + 1, operators) + ") " + op + " float(" + destructure_tree(tree[1][1], recursion_count + 1, operators) + "))"

		case "DIV":
			return "(float(" + destructure_tree(tree[1][0], recursion_count + 1, operators) + ") // float(" + destructure_tree(tree[1][1], recursion_count + 1, operators) + "))"
		
		case "MOD":
			return "(int(" + destructure_tree(tree[1][0], recursion_count + 1, operators) + ") \% int(" + destructure_tree(tree[1][1], recursion_count + 1, operators) + "))"

		case "=":
			return "(str(" + destructure_tree(tree[1][0], recursion_count + 1, operators) + ") == str(" + destructure_tree(tree[1][1], recursion_count + 1, operators) + "))"

		case "<>":
			return "(str(" + destructure_tree(tree[1][0], recursion_count + 1, operators) + ") != str(" + destructure_tree(tree[1][1], recursion_count + 1, operators) + "))"
		
		case "&":
			#print(tree)
			return '(str(' + destructure_tree(tree[1][0], recursion_count + 1, operators) + ") + str(" + destructure_tree(tree[1][1], recursion_count + 1, operators) + "))"
		
		case "IF" | "WHILE":
			cond = destructure_tree(tree[1][0], recursion_count + 1, operators)
			block = destructure_tree(tree[1][1], recursion_count + 1, operators)
			return "  " * recursion_count + op.lower() + " " + cond + ":\n" + block
		
		case "ELSE":
			return "  " * recursion_count + "else:\n" + destructure_tree(tree[1], recursion_count + 1, operators)
	
		case "FOR":
			c_blk = tree[1][0]
			var = c_blk[0]
			rg = 'range(' + c_blk[1] + ', ' + c_blk[2] + ', ' + c_blk[3] + ')'
			return "  " * recursion_count + "for " + var + " in " + rg + ":\n" + destructure_tree(tree[1][1], recursion_count + 1, operators)

		case "PROCEDURE" | "FUNCTION":
			f_decl = ""
			for arg in tree[1][1]:
				ident = arg[0]
				v_type = match_type(arg[1])
				f_decl += ident + ": " + v_type + ", "
			f_decl = f_decl[:-2]
			return "def " + tree[1][0] + "(" + f_decl + "):\n" + destructure_tree(tree[1][3], recursion_count + 1, operators)
		
		case "RETURN":
			return "  " * recursion_count + "return " + destructure_tree(tree[1], recursion_count + 1, operators) + "\n"

		case "OUTPUT":
			#out = ''
			#if type(tree[1][0]) == tuple:
			#	for (t, _) in enumerate(tree[1][0]):
			#		print(tree[1][0][t])
					#out += 'str(' + destructure_tree(tree[1][0][t], recursion_count + 1, operators) + ')'
			#else:
				#print(tree[1])
			#	out += 'str(' + tree[1][0] + ')'
			return "  " * recursion_count + "print(" + destructure_tree(tree[1][0], recursion_count + 1, operators) + ")\n"

		case _:
			return "  " * recursion_count + "uh oh stinky code nonononono"


def destructure_tree(tree: tuple, recursion_count: int, operators: list):
	#print(tree)
	left = tree[0]
	if type(left) == tuple:
		to_return = ''
		for t in tree:
			to_return += destructure_tree(t, recursion_count + 1, operators)
		return to_return
	else:
		if left in operators:
			return match_operator(tree, recursion_count, operators)
		else:
			return tree