# This source code only supports square matrix.
# This source code doesn't have exception handling.

import copy


class Matrix:
    def __init__(self, size, array):
        self.size = size
        self.iterSize = self.size + 1
        self.mat = [[0 for col in range(self.size+1)] for row in range(self.size+1)]

        if isinstance(array[0], list):
            self.mat = array

        else:
            m = 0
            for i in range(1, self.iterSize):
                for j in range(1, self.iterSize):
                    self.mat[i][j] = array[m]
                    m += 1

    def identity(size: int):
        array = [[0 for col in range(size+1)] for row in range(size+1)]

        for i in range(1, size+1):
            array[i][i] = 1
        
        return Matrix(size, array)
    
    def eye(size: int):
        return Matrix.identity(size)
        
    def zero(size: int):
        array = [[0 for col in range(size+1)] for row in range(size+1)]

        return Matrix(size, array)

    def __str__(self):
        return str(self.mat)

    # Operator overloading
    def __add__(self, other):
        newMatrix = copy.deepcopy(self)

        for i in range(1, newMatrix.iterSize):
            for j in range(1, newMatrix.iterSize):
                newMatrix.mat[i][j] += other.mat[i][j]
        
        return newMatrix
    
    def __sub__(self, other):
        newMatrix = copy.deepcopy(self)

        for i in range(1, newMatrix.iterSize):
            for j in range(1, newMatrix.iterSize):
                newMatrix.mat[i][j] -= other.mat[i][j]
        
        return newMatrix
    
    def __neg__(self):
        newMatrix = copy.deepcopy(self)

        for i in range(1, newMatrix.iterSize):
            for j in range(1, newMatrix.iterSize):
                newMatrix.mat[i][j] = -newMatrix.mat[i][j]
        
        return newMatrix

    def __mul__(self, other):
        if isinstance(other, Matrix):
            newMatrix = Matrix.identity(self.size)

            for i in range(1, newMatrix.iterSize):
                for j in range(1, newMatrix.iterSize):
                    newMatrix.mat[i][j] = 0
                    for m in range(1, newMatrix.iterSize):
                        newMatrix.mat[i][j] += self.mat[i][m] * other.mat[m][j]

            return newMatrix

        elif isinstance(other, int):
            newMatrix = copy.deepcopy(self)
            
            for i in range(1, newMatrix.iterSize):
                for j in range(1, newMatrix.iterSize):
                    newMatrix.mat[i][j] *= other
            
            return newMatrix
    
    def __pow__(self, other):
        newMatrix = copy.deepcopy(self)
        mat = copy.deepcopy(self)

        for i in range(other-1):
            newMatrix *= mat
        
        return newMatrix

    # Elementary row operation
    # Row switching transformation: switches all matrix elements on row i with their counterparts on row j. 
    def rowSwitch(self, i, j):
        newMatrix = copy.deepcopy(self)

        E = Matrix.identity(newMatrix.size)
        E.mat[i][i] = E.mat[j][j] = 0
        E.mat[i][j] = E.mat[j][i] = 1

        newMatrix = E * newMatrix

        return newMatrix

    # Row multifyling transformation: multiplies all elements on row i by m where m is a non-zero scalar.
    def rowMultifly(self, i, m):
        newMatrix = copy.deepcopy(self)

        E = Matrix.identity(newMatrix.size)
        E.mat[i][i] = m

        newMatrix = E * newMatrix

        return newMatrix

    # Row addition transformation: adds row j multiplied by a scalar m to row i.
    def rowAdd(self, j, m, i):
        newMatrix = copy.deepcopy(self)

        E = Matrix.identity(newMatrix.size)
        
        if (j == i):
            E.mat[i][i] = m+1
        else:
            E.mat[i][j] = m
        
        newMatrix = E * newMatrix

        return newMatrix

    def scriptMath(self): # use "from IPython.display import Math" code: Math(MatObject.scriptMath())
        script = "\\begin{bmatrix} "

        for i in range(1, self.iterSize):
            for j in range(1, self.iterSize):
                script = script + str(self.mat[j][i]) + "&"
            script += "& "
        
        script = script.replace("&&", "\\\\")
        script = script.rstrip("\\\\ ")
        script += " \\end{bmatrix}"

        return script

if __name__ == "__main__":
    a = Matrix(3)
    a.scriptMath()