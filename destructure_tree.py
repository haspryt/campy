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
					tail += "datetime.datetime.new()"
			return "  " * recursion_count + destructure_tree(tree[1][0], recursion_count + 1, operators) + tail + "\n"

		case "<-":
			return "  " * recursion_count + tree[1][0] + " = " + destructure_tree(tree[1][1], recursion_count + 1, operators) + "\n"
		
		case "<" | ">" | ">=" | "<=":
			return "(" + destructure_tree(tree[1][0], recursion_count + 1, operators) + " " + op + " " + destructure_tree(tree[1][1], recursion_count + 1, operators) + ")"
		
		case "=":
			return "(" + destructure_tree(tree[1][0], recursion_count + 1, operators) + " == " + destructure_tree(tree[1][1], recursion_count + 1, operators) + ")"

		case "<>":
			return "(" + destructure_tree(tree[1][0], recursion_count + 1, operators) + " != " + destructure_tree(tree[1][1], recursion_count + 1, operators) + ")"
		
		case "IF":
			cond = destructure_tree(tree[1][0], recursion_count + 1, operators)
			block = destructure_tree(tree[1][1], recursion_count + 1, operators)
			return "  " * recursion_count + "if " + cond + ":\n" + block
		
		case "ELSE":
			return "  " * recursion_count + "else:\n" + destructure_tree(tree[1], recursion_count + 1, operators)
		
		case "OUTPUT":
			return "  " * recursion_count + "print(" + destructure_tree(tree[1], recursion_count + 1, operators) + ")\n"


def destructure_tree(tree: tuple, recursion_count: int, operators: list):
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