# This source code only supports square matrix.
# This source code doesn't have exception handling.

import copy


class Matrix:
    def __init__(self, size, list = []):
        self.size = size
        self.iterRange = range(1, self.size+1)

        self.mat = [[0 for col in range(self.size+1)] for row in range(self.size+1)]

        if not list: # make identity matrix
            for i in self.iterRange:
                self.mat[i][i] = 1

        if isinstance(list[0], list):
            self.mat = list

        else:
            m = 0
            for i in self.iterRange:
                for j in self.iterRange:
                    self.mat[i][j] = list[m]

    def __str__(self):
        return str(self.mat)

    # Operator overloading
    def __add__(self, other):
        newMatrix = copy.deepcopy(self)

        for i in newMatrix.iterRange:
            for j in newMatrix.iterRange:
                newMatrix.mat[i][j] += other.mat[i][j]
        
        return newMatrix
    
    def __sub__(self, other):
        newMatrix = copy.deepcopy(self)

        for i in newMatrix.iterRange:
            for j in newMatrix.iterRange:
                newMatrix.mat[i][j] -= other.mat[i][j]
        
        return newMatrix
    
    def __neg__(self):
        newMatrix = copy.deepcopy(self)

        for i in newMatrix.iterRange:
            for j in newMatrix.iterRange:
                newMatrix.mat[i][j] = -newMatrix.mat[i][j]
        
        return newMatrix

    def __mul__(self, other):
        if isinstance(other, Matrix):
            newMatrix = Matrix(self.size)

            for i in newMatrix.iterRange:
                for j in newMatrix.iterRange:
                    newMatrix.mat[i][j] = 0
                    for m in newMatrix.iterRange:
                        newMatrix.mat[i][j] += self.mat[i][m] * other.mat[m][j]

            return newMatrix

        elif isinstance(other, int):
            newMatrix = copy.deepcopy(self)
            
            for i in newMatrix.iterRange:
                for j in newMatrix.iterRange:
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
    def rowSwitch(matrix, i, j):
        newMatrix = copy.deepcopy(matrix)

        E = Matrix(newMatrix.size)
        E.mat[i][i] = E.mat[j][j] = 0
        E.mat[i][j] = E.mat[j][i] = 1

        newMatrix = E * newMatrix

        return newMatrix

    # Row multifyling transformation: multiplies all elements on row i by m where m is a non-zero scalar.
    def rowMultifly(matrix, i, m):
        newMatrix = copy.deepcopy(matrix)

        E = Matrix(newMatrix.size)
        E.mat[i][i] = m

        newMatrix = E * newMatrix

        return newMatrix

    # Row addition transformation: adds row j multiplied by a scalar m to row i.
    def rowAdd(matrix, j, m, i):
        newMatrix = copy.deepcopy(matrix)

        E = Matrix(newMatrix.size)
        
        if (j == i):
            E.mat[i][i] = m+1
        else:
            E.mat[i][j] = m
        
        newMatrix = E * newMatrix

        return newMatrix
