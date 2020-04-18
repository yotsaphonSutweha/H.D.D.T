from pathlib import Path
from csv import reader 
from random import randrange
import os
import pandas as pd
import numpy as np
from MachineLearningModels.perceptron import Perceptron
from MachineLearningModels.knn import KNN
from MachineLearningModels.svm import SVM
from MachineLearningModels.perceptron_best_stats import PerceptronStats


stats = PerceptronStats()
perceptron = Perceptron()
knn = KNN()
svm = SVM()

def loadCsv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csvReader = reader(file)
        for row in csvReader:
            if not row:
                continue
            dataset.append(row)
    return dataset

def trainTestSplit(dataset, trainSplit = 0.75):
    train = list()
    trainSize = trainSplit * len(dataset)
    datasetCopy = list(dataset)
    while len(train) < trainSize:
        index = randrange(len(datasetCopy))
        train.append(datasetCopy.pop(index))
    return train, datasetCopy

def convertStringColumnToFloat(hd, column):
    for row in hd:
        row[column] = float(row[column].strip()) 

def convertStringColumnToInt(dataset, column):
    classValues = [row[column] for row in dataset]
    uniqueValues = set(classValues)
    lookup = dict()
    for i, value in enumerate(uniqueValues):
        lookup[value] = i
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup 

def accuracyMetric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0

def dataPreprocessing(filename):
    data = loadCsv(filename)
    hd = data[1: len(data)]
    for i in range(len(hd[0])-1):
        convertStringColumnToFloat(hd, i)
    convertStringColumnToInt(hd, len(hd[0])-1)
    dataTrain, dataTest = trainTestSplit(hd)
    return dataTrain, dataTest

def perceptronModel(dataTrain, dataTest, patientCondition, actualResults):
    lRate = 0.06
    nEpoch = 1000 
    weights = []
    bestWeights = []
    perceptronAccuracy = 0
    for i in range(0, 5):
        perceptronPredictions, weights = perceptron.buildPerceptron(dataTrain, dataTest, patientCondition, lRate, nEpoch)
        accuracy = perceptronEvaluation(perceptronPredictions, actualResults)
        if accuracy > perceptronAccuracy:
            perceptronAccuracy = accuracy
            bestWeights = weights
    return perceptronAccuracy, bestWeights

def knnModel(dataTrain, dataTest, patientCondition, actualResults):
    knnPredicts = list()
    for i in range(len(dataTest)):
        knnPrediction = knn.k_nearest_neighbours(dataTrain, dataTest[i], 5)
        knnPredicts.append(knnPrediction)
    knnAccuracy = accuracyMetric(actualResults, knnPredicts)
    patientDiagnosis = knn.k_nearest_neighbours(dataTrain, patientCondition, 5)
    return knnAccuracy, patientDiagnosis

def svmModel(dataTrain, dataTest, patientCondiction):
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    for i in dataTrain:
        X_train.append(i[:13])
        y_train.append(i[-1])

    for j in dataTest:
        X_test.append(j[:13])
        y_test.append(j[-1])

    svm.train(np.array(X_train), np.array(y_train))
    accuracy = svm.test(np.array(X_test), np.array(y_test))
    diagnosticResult = svm.predict([patientCondiction[:13]])

    accuracy = round(accuracy, 2)*100
    diagnosticResult = int(diagnosticResult[0])
    return diagnosticResult, accuracy

def perceptronEvaluation(perceptronPredictions, actualResults):
    intValsPerceptonPrecitions = list()
    for i in perceptronPredictions:
        intValsPerceptonPrecitions.append(int(i))
    perceptronAccuracy = accuracyMetric(actualResults, intValsPerceptonPrecitions)
    return perceptronAccuracy

# take a look closely at how each row is being handled by the models
def heartDiseaseDiagnosis(patient_conditions):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'data/cleavelandAndHungarianData.csv')
    trainDataset, testDataset = dataPreprocessing(filename)
    test = testDataset[len(testDataset)-1]
    # print(trainDataset)
    # print("Y: {0}".format(test))
    # print("X: {0}".format(patient_conditions))

    actualResults = list()
    for row in testDataset:
        actualResults.append(row[-1])

    perceptronAccuracy, weights = perceptronModel(trainDataset, testDataset, patient_conditions, actualResults)
    print(" Best accuracy: {0}".format(stats.get_accuracy()))
    print("Best weights: {0}".format(stats.get_weights()))
    temp = 0
    if perceptronAccuracy > stats.get_accuracy():
        patientDiagnosisPerceptron = perceptron.patientDiagnosis(patient_conditions, weights)
        stats.set_weights(weights)
        stats.set_accuracy(perceptronAccuracy)
    else:
        patientDiagnosisPerceptron = perceptron.patientDiagnosis(patient_conditions, stats.get_weights())
        perceptronAccuracy = stats.get_accuracy()
        print("Use the old weights with the accuracy of {0}".format(perceptronAccuracy))

    knnAccuracy, patientDiagnosisKNN = knnModel(trainDataset, testDataset, patient_conditions, actualResults)

    svmDiagnosticResult, svmDiagnosticAccuracy = svmModel(trainDataset, testDataset, patient_conditions)
    # svmDiagnosticResult = 0
    # svmDiagnosticAccuracy = 0
   
    return perceptronAccuracy, patientDiagnosisPerceptron, knnAccuracy, patientDiagnosisKNN, svmDiagnosticAccuracy, svmDiagnosticResult



# condition = [57,1,4,130,131,0,0,115,1,1.2,2,1,1]
# heartDiseaseDiagnosis(condition)

# perceptronAcc, patientDiagnosisPerceptron, knnAcc, patientdiagnosisKNN = heartDiseaseDiagnosis(condition)

# print('Perceptron acc: {0}, Perceptron prediction: {1}, KNNAcc: {2}, KNNPrediction: {3}'.format(perceptronAcc, patientDiagnosisPerceptron, knnAcc, patientdiagnosisKNN))

# res = 1

# heartDiseaseDiagnosis(condition)