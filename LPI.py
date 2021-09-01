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


    def calc(self, steps=False, prec=1):
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
            "final_expression": L.evalf(prec),
            "simplified_expression": func.evalf(prec),
        }

        return output

    def plotter(self, eq):
        # plotting original data
        X_cont = np.linspace(self.xmin, self.xmax, self.n*10)
        Y_cont = np.zeros(len(X_cont))

        for i in range(len(Y_cont)):
            Y_cont[i] = eq.subs({self.var:X_cont[i]})

        plt.style.use('seaborn-whitegrid')
        p_points = plt.plot(self.X, self.Y, marker='o',linestyle=' ')
        p_cont = plt.plot(X_cont, Y_cont, marker='',linestyle='-')
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.savefig('plot.png')

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
    pprint(output["simplified_expression"])

    poly.to_file(output)
    poly.plotter(output['simplified_expression'])

    t_end = time.time()

    dt = t_end - t_start
    print(f'\ntime taken: {dt:.2f}s')


if __name__ == "__main__":
    main()