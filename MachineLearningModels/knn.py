from math import *
import numpy as np
class KNN:
    def __init__(self):
        super().__init__()

    def euclideanDistance(self, row1, row2):
        distance = 0.0
        for i in range(len(row1)-1):
            distance += (row1[i] - row2[i])**2
        return sqrt(distance)

    def getNeighbours(self, train, testRow, numNeighbours):
        distances = list()
        for trainRow in train:
            distance = self.euclideanDistance(testRow, trainRow)
            distances.append((trainRow, distance))
        distances.sort(key=lambda tup: tup[1])
        neighbours = list()
        for i in range(numNeighbours):
            neighbours.append(distances[i][0])
        return neighbours

    def buildKnn(self, train, testRow, k):
        neighbours = self.getNeighbours(train, testRow, k)
        outputVals = [row[-1] for row in neighbours]
        prediction = max(set(outputVals), key=outputVals.count)
        return prediction