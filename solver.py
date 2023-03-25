import re
import sympy as sym
from keras.models import model_from_json
import numpy as np
import cv2
from segmentation import segment_image, segment_lines


def show_image(img):
    cv2.imshow("preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def load_model():
    with open("Models/solver_model.json", 'r') as json_file:
        solver_model = model_from_json(json_file.read())
    solver_model.load_weights("Models/solver_model_weights.h5")

    return solver_model


def extract(img):
    solver_model = load_model()

    segmented_symbols = segment_image(img)

    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '=', 'x', 'y']
    expression = ""
    for i in range(len(segmented_symbols)):
        segmented_symbols[i] = np.array(segmented_symbols[i]).astype('float32')
        segmented_symbols[i] = segmented_symbols[i].reshape((1, 28, 28, 1))/255
        result = solver_model.predict(segmented_symbols[i]).argmax()
        expression += classes[result]

    return expression


def extract_linear_equations(img):
    lines = segment_lines(img)

    equations = ""
    for line in lines:
        equations += extract(line) + '\n'

    return equations[:-1]


def solve_expression(expression):
    solution = str(eval(expression))

    return solution


def solve_linear_equation(equation):
    equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
    equation = re.sub(r"(x)(\d)", r"\1**\2", equation)

    expression, value = equation.split('=')
    equation_string = expression + '=' + value

    expression = sym.sympify(expression)
    equation = sym.Eq(expression, int(value))

    roots = sym.solve(equation)

    solution = ""
    for root in roots:
        solution += "x = " + str(root).replace("I", "i") + ",\n"

    return equation_string, solution[:-2]


def solve_linear_system(equations):
    equations = equations.split("\n")
    x, y = sym.symbols('x y')

    system = []
    for equation in equations:
        equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
        equation = re.sub(r"(\d)(y)", r"\1*\2", equation)

        expression, value = equation.split('=')
        expression = sym.sympify(expression)

        equation = sym.Eq(expression, int(value))

        system.append(equation)

    solutions = sym.linsolve(system, x, y)
    if solutions:
        solution = f"x = {solutions.args[0][0]},\ny = {solutions.args[0][1]}"

        return solution
    else:
        return "No Solution"


def differentiate(equation):
    x = sym.symbols('x')

    equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
    equation = re.sub(r"(x)(\d)", r"\1**\2", equation)

    equation = sym.sympify(equation)

    solution = str(sym.diff(equation, x))

    return solution


def indefinite_integral(equation):
    equation = equation[1:-2]
    x = sym.symbols('x')

    equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
    equation = re.sub(r"(x)(\d)", r"\1**\2", equation)

    equation = sym.sympify(equation)

    solution = str(sym.integrate(equation, x))

    return solution + " + C"


def definite_integral(equation):
    lower = equation[0]
    upper = equation[2]
    equation = equation[3:-2]
    x = sym.symbols('x')

    equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
    equation = re.sub(r"(x)(\d)", r"\1**\2", equation)

    equation = sym.sympify(equation)

    solution = str(sym.integrate(equation, (x, lower, upper)))

    return solution


if __name__ == '__main__':
    image = cv2.imread("")
    show_image(image)
    eq = extract(image)
    sol = definite_integral(eq)
    print(f"Expression: {eq}\n Solution: {sol}")
