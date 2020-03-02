from math import *
import numpy as np

def euclideanDistance(row1, row2):
    distance = 0.0
    for i in range(len(row1)-1):
        distance += (row1[i] - row2[i])**2
    return sqrt(distance)

def getNeighbours(train, testRow, numNeighbours):
    distances = list()
    for trainRow in train:
        distance = euclideanDistance(testRow, trainRow)
        distances.append((trainRow, distance))
    distances.sort(key=lambda tup: tup[1])
    neighbours = list()
    for i in range(numNeighbours):
        neighbours.append(distances[i][0])
    return neighbours

def buildKnn(train, testRow, k):
    neighbours = getNeighbours(train, testRow, k)
    outputVals = [row[-1] for row in neighbours]
    prediction = max(set(outputVals), key=outputVals.count)
    return prediction