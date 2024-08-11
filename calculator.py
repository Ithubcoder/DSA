import math

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        raise ValueError("Division by zero is not allowed")

def power(x, y):
    return x ** y

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def sqrt(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        raise ValueError("Cannot take square root of a negative number")

def log(x):
    if x > 0:
        return math.log10(x)
    else:
        raise ValueError("Logarithm undefined for non-positive values")

def ln(x):
    if x > 0:
        return math.log(x)
    else:
        raise ValueError("Natural logarithm undefined for non-positive values")

def tokenize(expression):
    tokens = []
    current_token = ""
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isdigit() or char == ".":
            current_token += char
        else:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            if char in "+-*/^()":
                tokens.append(char)
            elif char.isalpha():
                while i < len(expression) and expression[i].isalpha():
                    current_token += expression[i]
                    i += 1
                tokens.append(current_token)
                current_token = ""
                continue
        i += 1
    if current_token:
        tokens.append(current_token)
    return tokens

def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    if op == '^':
        return 3
    return 0

def infix_to_postfix(expression):
    stack = Stack()
    postfix = []
    tokens = tokenize(expression)

    for token in tokens:
        if token.isdigit() or '.' in token:
            postfix.append(token)
        elif token.isalpha():
            postfix.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            while (not stack.is_empty() and precedence(token) <= precedence(stack.peek())):
                postfix.append(stack.pop())
            stack.push(token)

    while not stack.is_empty():
        postfix.append(stack.pop())

    return postfix

def evaluate_postfix(postfix, variables={}):
    stack = Stack()

    for token in postfix:
        if token.isdigit() or '.' in token:
            stack.push(float(token))
        elif token in variables:
            stack.push(variables[token])
        elif token in ('sin', 'cos', 'tan', 'sqrt', 'log', 'ln'):
            x = stack.pop()
            if token == 'sin':
                result = sin(x)
            elif token == 'cos':
                result = cos(x)
            elif token == 'tan':
                result = tan(x)
            elif token == 'sqrt':
                result = sqrt(x)
            elif token == 'log':
                result = log(x)
            elif token == 'ln':
                result = ln(x)
            stack.push(result)
        else:
            y = stack.pop()
            x = stack.pop()
            if token == '+':
                result = add(x, y)
            elif token == '-':
                result = subtract(x, y)
            elif token == '*':
                result = multiply(x, y)
            elif token == '/':
                result = divide(x, y)
            elif token == '^':
                result = power(x, y)
            stack.push(result)

    return stack.pop()

def calculator(expression, variables={}):
    try:
        postfix = infix_to_postfix(expression)
        result = evaluate_postfix(postfix, variables)
        return result
    except ValueError as e:
        return str(e)
    except Exception as e:
        return "Invalid input"

if __name__ == "__main__":
    history = []
    variables = {}
    while True:
        expression = input("Enter an arithmetic expression (or type 'exit' to quit): ")
        if expression.lower() == "exit":
            break
        if "=" in expression:
            var_name, var_expr = expression.split("=")
            var_name = var_name.strip()
            var_value = calculator(var_expr.strip(), variables)
            if isinstance(var_value, (int, float)):
                variables[var_name] = var_value
                print(f"{var_name} = {var_value}")
            else:
                print(var_value)
        else:
            result = calculator(expression, variables)
            print(f"Result: {result}")
            history.append((expression, result))

    print("\nCalculation History:")
    for expr, res in history:
        print(f"{expr} = {res}")
