import pytest
from app.rule_engine import create_rule, combine_rules, evaluate_rule

def test_create_rule():
    rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    ast1 = create_rule(rule1)
    assert ast1.type == "operator"
    assert ast1.value == "AND"
    assert ast1.left.type == "operator"
    assert ast1.left.value == "OR"
    assert ast1.right.type == "operator"
    assert ast1.right.value == "OR"

def test_combine_rules():
    rule1 = "age > 30 AND department = 'Sales'"
    rule2 = "salary > 50000 OR experience > 5"
    combined = combine_rules([rule1, rule2])
    assert combined.type == "operator"
    assert combined.value == "AND"
    assert combined.left.value == "AND"
    assert combined.right.value == "OR"

def test_evaluate_rule():
    rule = create_rule("age > 30 AND department = 'Sales'")
    data1 = {"age": 35, "department": "Sales"}
    data2 = {"age": 25, "department": "Sales"}
    assert evaluate_rule(rule.to_dict(), data1) == True
    assert evaluate_rule(rule.to_dict(), data2) == False
    
# Test case for creating a rule
rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))"
ast = create_rule(rule_string)
assert ast is not None

# Test case for combining rules
combined_ast = combine_rules([rule1, rule2])
assert combined_ast is not None

# Test case for evaluating a rule
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
result = evaluate_rule(ast.to_dict(), data)
assert result is True


# Add more test cases for error handling, attribute validation, and rule modification