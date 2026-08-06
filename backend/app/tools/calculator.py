import ast
import operator


operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def evaluate(node):

    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        return operators[type(node.op)](
            evaluate(node.left),
            evaluate(node.right)
        )

    if isinstance(node, ast.UnaryOp):
        return operators[type(node.op)](
            evaluate(node.operand)
        )

    raise ValueError("Invalid Expression")


def calculator(expression: str):

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = evaluate(tree.body)

        return str(result)

    except Exception:

        return "Invalid mathematical expression."