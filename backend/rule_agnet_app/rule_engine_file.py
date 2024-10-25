import re
from typing import List, Dict, Any

class InvalidRuleException(Exception):
    pass

class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type  # "operator" or "operand"
        self.value = value  # E.g., "AND", "age > 30"
        self.left = left  # Reference to the left child node
        self.right = right  # Reference to the right child node

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

def create_rule(rule_string: str) -> Node:
    def parse_expression(tokens):
        if not tokens:
            raise InvalidRuleException("Empty expression")

        if tokens[0] == '(':
            left, left_pos = parse_expression(tokens[1:])
            if left_pos + 1 >= len(tokens):
                raise InvalidRuleException("Incomplete expression: missing operator or right operand.")
            op = tokens[left_pos + 1]
            right, right_pos = parse_expression(tokens[left_pos + 2:])
            return Node("operator", op, left, right), left_pos + right_pos + 3
        else:
            if len(tokens) < 3:
                raise InvalidRuleException("Invalid operand format.")
            attr, op, value = tokens[0], tokens[1], tokens[2]
            return Node("operand", f"{attr} {op} {value}"), 3

    # Updated regex to also recognize '=' operator
    tokens = re.findall(r'\(|\)|AND|OR|[\w.]+|>=|<=|>|<|=|!=', rule_string)
    if not tokens:
        raise InvalidRuleException("Empty rule string.")
    ast, _ = parse_expression(tokens)
    return ast

def evaluate_rule(ast_json: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """Evaluates the rule represented by the AST against the provided data."""
    def evaluate_node(node: Dict[str, Any]) -> bool:
        if node["type"] == "operand":
            # Split the operand into attribute, operator, and value
            match = re.match(r"([\w.]+) (>=|<=|>|<|=|!=) (.+)", node["value"])
            if not match:
                raise InvalidRuleException(f"Invalid operand: {node['value']}")
            
            attr, operator, value = match.groups()
            if attr not in data:
                raise InvalidRuleException(f"Attribute {attr} not found in data.")
            
            # Convert data and value to appropriate types for comparison
            data_value = data[attr]
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Keep value as a string if it can't be converted
            
            # Perform the comparison based on the operator
            if operator == ">=":
                return data_value >= value
            elif operator == "<=":
                return data_value <= value
            elif operator == ">":
                return data_value > value
            elif operator == "<":
                return data_value < value
            elif operator == "=":
                return data_value == value
            elif operator == "!=":
                return data_value != value
            else:
                raise InvalidRuleException(f"Unsupported operator: {operator}")
        elif node["type"] == "operator":
            left_result = evaluate_node(node["left"])
            right_result = evaluate_node(node["right"])
            if node["value"] == "AND":
                return left_result and right_result
            elif node["value"] == "OR":
                return left_result or right_result
            else:
                raise InvalidRuleException(f"Unsupported logical operator: {node['value']}")
        else:
            raise InvalidRuleException(f"Unknown node type: {node['type']}")

    return evaluate_node(ast_json)

# import re
# import ast
# from typing import List, Dict, Any

# class InvalidRuleException(Exception):
#     """Custom exception for invalid rule expressions."""
#     pass

# class Node:
#     """Represents a node in the Abstract Syntax Tree (AST)."""
#     def __init__(self, type, value=None, left=None, right=None):
#         self.type = type  # "operator" or "operand"
#         self.value = value  # E.g., "AND", "age > 30"
#         self.left = left  # Reference to the left child node
#         self.right = right  # Reference to the right child node

#     def to_dict(self):
#         return {
#             "type": self.type,
#             "value": self.value,
#             "left": self.left.to_dict() if self.left else None,
#             "right": self.right.to_dict() if self.right else None
#         }
        
#     def __eq__(self, other: 'Node') -> bool:
#         """Checks if two nodes are equal based on type, value, and children."""
#         if not isinstance(other, Node):
#             return False
#         return (
#             self.type == other.type and
#             self.value == other.value and
#             self.left == other.left and
#             self.right == other.right
#         )

# def create_rule(rule_string: str) -> Node:    
#     """
#     Parses a rule string and converts it to an Abstract Syntax Tree (AST).
    
#     :param rule_string: The string representation of the rule.
#     :return: The root node of the AST.
#     :raises InvalidRuleException: If the rule string is invalid.
#     """
#     def parse_expression(tokens):
#         if not tokens:
#             raise InvalidRuleException("Empty expression")

#         if tokens[0] == '(':
#             left, left_pos = parse_expression(tokens[1:])
#             if left_pos + 1 >= len(tokens):
#                 raise InvalidRuleException("Incomplete expression: missing operator or right operand.")
#             op = tokens[left_pos + 1]
#             right, right_pos = parse_expression(tokens[left_pos + 2:])
#             return Node("operator", op, left, right), left_pos + right_pos + 3
#         else:
#             if len(tokens) < 3:
#                 raise InvalidRuleException("Invalid operand format.")
#             attr, op, value = tokens[0], tokens[1], tokens[2]
#             return Node("operand", f"{attr} {op} {value}"), 3

#     # Updated regex to also recognize '=' operator
#     tokens = re.findall(r'\(|\)|AND|OR|[\w.]+|>=|<=|>|<|=|!=', rule_string)
#     if not tokens:
#         raise InvalidRuleException("Empty rule string.")
#     ast, _ = parse_expression(tokens)
#     return ast

# def combine_rules(rules: List[str]) -> Node:
#     """
#     Combines multiple rules into a single AST.
    
#     :param rules: List of rule strings.
#     :return: Combined AST root node.
#     :raises ValueError: If no rules are provided.
#     """
    
#     if not rules:
#         raise ValueError("No rules provided.")
    
#     # Parse all rules into their AST representations
#     ast_list = [create_rule(rule) for rule in rules]

#     # Use a heuristic to decide how to combine them
#     # For example, if "OR" is more common, use it as the primary operator
#     and_count = sum(1 for rule in rules if "AND" in rule)
#     or_count = len(rules) - and_count
#     primary_operator = "OR" if or_count > and_count else "AND"

#     # Combine the ASTs using the primary operator
#     combined_ast = ast_list[0]
#     for ast in ast_list[1:]:
#         combined_ast = Node("operator", primary_operator, combined_ast, ast)
    
#     # Optional: Further optimization by removing duplicate nodes
#     combined_ast = optimize_ast(combined_ast)
#     return combined_ast

# def optimize_ast(node: Node) -> Node:
#     """
#     Recursively optimizes the AST by removing redundant nodes.
    
#     :param node: The current node of the AST.
#     :return: Optimized AST node.
#     """
#     if node.type == "operator":
#         left = optimize_ast(node.left)
#         right = optimize_ast(node.right)

#         # If the left and right sub-trees are the same, we can reduce the depth
#         if left == right:
#             return left

#         # Simplify nested identical operators, e.g., ((A AND B) AND C)
#         if node.left.type == node.type and node.right.type == node.type:
#             return Node(node.type, node.value, left.left, Node(node.type, node.value, left.right, right))
        
#         return Node(node.type, node.value, left, right)
#     else:
#         # Return leaf node (operand) as is
#         return node


# # def combine_rules(rules: List[str]) -> Node:
# #     if not rules:
# #         raise ValueError("No rules provided.")
# #     if len(rules) == 1:
# #         return create_rule(rules[0])

# #     combined_ast = create_rule(rules[0])
# #     for rule in rules[1:]:
# #         new_ast = create_rule(rule)
# #         combined_ast = Node("operator", "AND", combined_ast, new_ast)  # Use "AND" to combine rules

# #     return combined_ast

# def evaluate_rule(ast: Dict[str, Any], data: Dict[str, Any]) -> bool:
#     """
#     Evaluates the given AST against the provided data.
    
#     :param ast: The AST representation of the rule.
#     :param data: The input data to evaluate the rule against.
#     :return: Boolean indicating if the rule matches the data.
#     """
#     def evaluate_node(node: Dict[str, Any]) -> bool:
#         if node["type"] == "operand":
#             # Split the operand into attribute, operator, and value
#             match = re.match(r"([\w.]+) (>=|<=|>|<|=|!=) (.+)", node["value"])
#             if not match:
#                 raise InvalidRuleException(f"Invalid operand: {node['value']}")
            
#             attr, operator, value = match.groups()
#             if attr not in data:
#                 raise InvalidRuleException(f"Attribute {attr} not found in data.")
            
#             # Convert data and value to appropriate types for comparison
#             data_value = data[attr]
#             try:
#                 value = int(value)
#             except ValueError:
#                 try:
#                     value = float(value)
#                 except ValueError:
#                     pass  # Keep value as a string if it can't be converted
            
#             # Perform the comparison based on the operator
#             if operator == ">=":
#                 return data_value >= value
#             elif operator == "<=":
#                 return data_value <= value
#             elif operator == ">":
#                 return data_value > value
#             elif operator == "<":
#                 return data_value < value
#             elif operator == "=":
#                 return data_value == value
#             elif operator == "!=":
#                 return data_value != value
#             else:
#                 raise InvalidRuleException(f"Unsupported operator: {operator}")
#         elif node["type"] == "operator":
#             left_result = evaluate_node(node["left"])
#             right_result = evaluate_node(node["right"])
#             if node["value"] == "AND":
#                 return left_result and right_result
#             elif node["value"] == "OR":
#                 return left_result or right_result
#             else:
#                 raise InvalidRuleException(f"Unsupported logical operator: {node['value']}")
#         else:
#             raise InvalidRuleException(f"Unknown node type: {node['type']}")

#     return evaluate_node(ast_json, data)

# # def evaluate_rule(ast: Dict[str, Any], data: Dict[str, Any]) -> bool:
# #     def evaluate_node(node):
# #         if node['type'] == 'operator':
# #             left = evaluate_node(node['left'])
# #             right = evaluate_node(node['right'])
# #             if node['value'] == 'AND':
# #                 return left and right
# #             elif node['value'] == 'OR':
# #                 return left or right
# #             else:
# #                 raise ValueError(f"Unknown operator: {node['value']}")
# #         elif node['type'] == 'operand':
# #             try:
# #                 attr, op, value = node['value'].split()
# #                 attr_value = data.get(attr)
# #                 if attr_value is None:
# #                     return False
                
                
# #                 # Perform comparison based on the operator
# #                 if op == '=':
# #                     return str(attr_value) == value.strip("'")
# #                 elif op == '!=':
# #                     return str(attr_value) != value.strip("'")
# #                 elif op == '>':
# #                     return float(attr_value) > float(value)
# #                 elif op == '<':
# #                     return float(attr_value) < float(value)
# #                 elif op == '>=':
# #                     return float(attr_value) >= float(value)
# #                 elif op == '<=':
# #                     return float(attr_value) <= float(value)
# #                 else:
# #                     raise ValueError(f"Invalid operator: {op}")
# #             except Exception as e:
# #                 raise ValueError(f"Error evaluating operand: {node['value']} - {str(e)}")

# #     return evaluate_node(ast)


# # # Sample rules
# # sample_rules = [
# #     "((age < 40 AND department = 'Engineering') OR (age >= 50 AND department = 'Finance')) AND (salary > 60000 AND experience > 10)",
# #     "((age >= 28 AND department = 'HR') OR (age < 30 AND department = 'IT')) AND (salary < 45000 OR experience <= 3)",
# #     "((age > 35 AND department = 'Operations') OR (age <= 22 AND department = 'Customer Service')) AND (salary >= 70000 AND experience >= 8)",
# #     "((age < 45 AND department = 'Research') OR (age = 30 AND department = 'Development')) AND (salary > 55000 OR experience < 5)",
# #     "((age > 32 AND department = 'Legal') AND (salary < 80000 AND experience >= 7)) OR (age < 28 AND department = 'Support' AND experience < 3)",
# #     "((age >= 26 AND department = 'Admin') OR (age > 50 AND department = 'Quality Assurance')) AND (salary <= 60000 OR experience > 12)",
# #     "((age < 38 AND department = 'Logistics') OR (age >= 45 AND department = 'Procurement')) AND (salary > 40000 AND experience >= 6)",
# #     "((age > 25 AND department = 'Technical') AND (salary > 30000 AND experience < 4)) OR (age < 23 AND department = 'Training' AND salary < 35000)"
# # ]