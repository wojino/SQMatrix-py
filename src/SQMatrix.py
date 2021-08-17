# This source code only supports square matrix.
# This source code doesn't have exception handling.

import copy
from fractions import Fraction


class Matrix:
    def __init__(self, size: int, array):
        self.size = size
        self.mat = [[Fraction(0) for col in range(self.size+1)] for row in range(self.size+1)]

        if isinstance(array[0], list):
            for i in range(1, self.size+1):
                for j in range(1, self.size+1):
                    self.mat[i][j] = Fraction(array[i-1][j-1])

        else:
            m = 0
            for i in range(1, self.size+1):
                for j in range(1, self.size+1):
                    self.mat[i][j] = Fraction(array[m])
                    m += 1

    def __str__(self):
        list = [[Fraction(0) for col in range(self.size)] for row in range(self.size)]

        for i in range(1, self.size+1):
            for j in range(1, self.size+1):
                list[i-1][j-1] = self.mat[i][j]
        return str(list)
    
    def script(self):
        # use "from IPython.display import Math" code: Math(MatObject.scriptMath())
        script = "\\begin{bmatrix} "

        for i in range(1, self.size+1):
            for j in range(1, self.size+1):
                script = script + str(self.mat[j][i]) + "&"
            script += "& "
        
        script = script.replace("&&", "\\\\")
        script = script.rstrip("\\\\ ")
        script += " \\end{bmatrix}"

        return script

    def identity(size: int):
        array = [[0 for col in range(size)] for row in range(size)]

        for i in range(0, size):
            array[i][i] = 1
        
        return Matrix(size, array)
    
    def eye(size: int):
        return Matrix.identity(size)
        
    def zero(size: int):
        array = [[0 for col in range(size)] for row in range(size)]

        return Matrix(size, array)

    # Operator overloading
    def __add__(self, other):
        newMatrix = copy.deepcopy(self)

        for i in range(1, newMatrix.size+1):
            for j in range(1, newMatrix.size+1):
                newMatrix.mat[i][j] += other.mat[i][j]
        
        return newMatrix
    
    def __sub__(self, other):
        newMatrix = copy.deepcopy(self)

        for i in range(1, newMatrix.size+1):
            for j in range(1, newMatrix.size+1):
                newMatrix.mat[i][j] -= other.mat[i][j]
        
        return newMatrix
    
    def __neg__(self):
        newMatrix = copy.deepcopy(self)

        for i in range(1, newMatrix.size+1):
            for j in range(1, newMatrix.size+1):
                newMatrix.mat[i][j] = -newMatrix.mat[i][j]
        
        return newMatrix

    def __mul__(self, other):
        if isinstance(other, Matrix):
            newMatrix = Matrix.identity(self.size)

            for i in range(1, newMatrix.size+1):
                for j in range(1, newMatrix.size+1):
                    newMatrix.mat[i][j] = 0
                    for m in range(1, newMatrix.size+1):
                        newMatrix.mat[i][j] += self.mat[i][m] * other.mat[m][j]

            return newMatrix

        elif isinstance(other, int):
            newMatrix = copy.deepcopy(self)
            
            for i in range(1, newMatrix.size+1):
                for j in range(1, newMatrix.size+1):
                    newMatrix.mat[i][j] *= other
            
            return newMatrix
    
    def __pow__(self, other):
        newMatrix = copy.deepcopy(self)
        mat = copy.deepcopy(self)

        for i in range(other-1):
            newMatrix *= mat
        
        return newMatrix

    def __eq__(self, other):
        return self.mat == other.mat

    def __ne__(self, other):
        return self.mat != other.mat

    # Elementary row operation
    def rowSwitch(self, i, j):
        # Row switching transformation: switches all matrix elements on row i with their counterparts on row j.

        newMatrix = copy.deepcopy(self)

        E = Matrix.identity(newMatrix.size)
        E.mat[i][i] = E.mat[j][j] = 0
        E.mat[i][j] = E.mat[j][i] = 1

        newMatrix = E * newMatrix

        return newMatrix

    def rowMultifly(self, i, m):
        # Row multifyling transformation: multiplies all elements on row i by m where m is a non-zero scalar.

        newMatrix = copy.deepcopy(self)

        E = Matrix.identity(newMatrix.size)
        E.mat[i][i] = m

        newMatrix = E * newMatrix

        return newMatrix
 
    def rowAdd(self, j, m, i):
        # Row addition transformation: adds row j multiplied by a scalar m to row i.

        newMatrix = copy.deepcopy(self)

        E = Matrix.identity(newMatrix.size)
        
        if (j == i):
            E.mat[i][i] = m+1
        else:
            E.mat[i][j] = m
        
        newMatrix = E * newMatrix

        return newMatrix

    def inv(self):
        A = copy.deepcopy(self)
        newMatrix = Matrix.identity(self.size)

        for i in range(1, A.size):
            for j in range(i+1, A.size+1):
                m = - A.mat[j][i] / A.mat[i][i]
                A = A.rowAdd(i, m, j)
                newMatrix = newMatrix.rowAdd(i, m, j)
        
        for i in range(1, A.size+1):
            m = 1/ A.mat[i][i]
            A = A.rowMultifly(i, m)
            newMatrix = newMatrix.rowMultifly(i, m)
        
        for i in range(2, A.size+1):
            for j in range(1, i):
                m = - A.mat[j][i] / A.mat[i][i]
                A = A.rowAdd(i, m, j)
                newMatrix = newMatrix.rowAdd(i, m, j)

        return newMatrix
    
    def t(self):
        newMatrix = Matrix.zero(self.size)

        for i in range(1, newMatrix.size+1):
            for j in range(1, newMatrix.size+1):
                newMatrix.mat[i][j] = self.mat[j][i]
        
        return newMatrix
    
    # decompositions
    def lu(self, method: str):

        if method == "gauss":
            U = copy.deepcopy(self)
            E = Matrix.identity(self.size)
            
            for i in range(1, U.size):
                for j in range(i+1, U.size+1):

                    m = - U.mat[j][i] / U.mat[i][i]
                    U = U.rowAdd(i, m, j)
                    E = E.rowAdd(i, m, j)

            L = E.inv()

            return (L, U)
        
        elif method == "doolittle":
            L = Matrix.identity(self.size)
            U = Matrix.identity(self.size)

            for k in range(1, self.size+1):
                L.mat[k][k] = 1

                for j in range(k, self.size+1):
                    sum = 0

                    for s in range(k):
                        sum += L.mat[k][s] * U.mat[s][j]

                    U.mat[k][j] = self.mat[k][j] - sum
                
                for i in range(k+1, self.size+1):
                    sum = 0

                    for s in range(k):
                        sum += L.mat[i][s] * U.mat[s][k]
                    
                    L.mat[i][k] = (self.mat[i][k] - sum) / U.mat[k][k]

            return (L, U)
    
    def plu(self):
        A = copy.deepcopy(self)
        P = Matrix.identity(A.size)

        for i in range(1, A.size+1):

            if A.mat[i][i] == 0:
                for j in range(i, A.size+1):
                    if A.mat[j][i] != 0:
                        A.rowSwitch(i, j)
                        P.rowSwitch(i, j)
                        break
        
        L, U = A.lu("doolittle")

        return (P, L, U)



if __name__ == "__main__":
    a = Matrix(3)
    a.scriptMath()