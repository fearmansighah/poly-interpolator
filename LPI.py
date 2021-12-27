import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import time
import csv
import pandas as pd

def csv_to_array(filename):
    df = pd.read_csv(filename)

    return df['X'], df['Y']

def get_var(var):

    return var

class interpolator:
    def __init__(self, var, X, Y):
        self.var = symbols(var)
        self.xmin = min(X)
        self.xmax = max(X)
        self.n = len(X)
        self.X = X
        self.Y = Y

        print(f'Attributes:\nvar = {self.var} | xmin = {self.xmin} |  xmax = {self.xmax} | n = {self.n}\n')
        print(f'X:\n{self.X}\n')
        print(f'Y:\n{self.Y}')


    def calc(self, steps=False):
        L = 0  # initialise L = 0
        print("\ncalculating...\n")
        for j in range(self.n):  # summation operator

            if steps is True:
                print("---------- j=", j, " ----------", sep="")
            else:
                pass

            product = 1  # reset product for each next j-th iteration
            for m in range(self.n):  # product operator
                if m == j:
                    continue  # skip to next j+1-th iteration if true
                product = product * (self.var - self.X[m]) / (self.X[j] - self.X[m])

                if steps is True:
                    print("m=", m, ": ", product, sep="")
                else:
                    pass

            if steps is True:
                print("j=", j, ": ", product * self.Y[j], sep="")
                print("j=", j, " (simplified): ", expand(product * self.Y[j]), sep="")
            else:
                pass

            L = L + self.Y[j] * product

        func = expand(L)

        output = {
            "final_expression": L,
            "simplified_expression": func,
        }

        return output['simplified_expression']


    def reformat(self, eq, prec):
        reformated_eq = eq.as_coefficients_dict()

        latex_var = f'${self.var}$'

        latex_eq = f'$f({latex_var}) = '
        iteration = 0
        for k, v in reversed(reformated_eq.items()):
            iteration += 1
            k = str(k).replace("**", "^")
            if v > 1 and v < 1:
                v = round(v, prec) 
            if iteration > 1 and v > 0:
                v = f'+{v}'   
            latex_eq += f'{v}{k}'
        latex_eq += '$'

        return latex_eq, latex_var


    def plotter(self, eq, latex_eq, latex_var):
        # plotting original data
        X_cont = np.linspace(self.xmin, self.xmax, self.n*10)
        Y_cont = np.zeros(len(X_cont))

        for i in range(len(Y_cont)):
            Y_cont[i] = eq.subs({self.var:X_cont[i]})

        plt.style.use('seaborn-whitegrid')
        p_points = plt.plot(self.X, self.Y, marker='o',linestyle=' ')
        p_cont = plt.plot(X_cont, Y_cont, marker='',linestyle='-')
        plt.xlabel(latex_var)
        plt.ylabel(latex_eq)
        plt.savefig('static/plot.png')

    def to_file(self, eq):
        f = open("output.txt", "w")
        f.write(str(eq))
        f.close


def main():
    t_start = time.time()

    X, Y = csv_to_array("xy.csv")
    var = get_var('x')

    poly = interpolator(var, X, Y)

    output = poly.calc()
    pprint(output)

    latex_eq, latex_var = poly.reformat(output, 2)

    poly.to_file(output)
    poly.plotter(output, latex_eq, latex_var)

    t_end = time.time()

    dt = t_end - t_start
    print(f'\ntime taken: {dt:.2f}s')


if __name__ == "__main__":
    main()