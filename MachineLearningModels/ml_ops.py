from MachineLearningModels.perceptron import Perceptron
from MachineLearningModels.knn import KNN
class MLops:
    def __init__(self, name):
        self.name = name
        
    def loadCsv(self, filename):
        dataset = list()
        with open(filename, 'r') as file:
            csvReader = reader(file)
            for row in csvReader:
                if not row:
                    continue
                dataset.append(row)
        return dataset

    def trainTestSplit(self, dataset, trainSplit = 0.75):
        train = list()
        trainSize = trainSplit * len(dataset)
        datasetCopy = list(dataset)
        while len(train) < trainSize:
            index = randrange(len(datasetCopy))
            train.append(datasetCopy.pop(index))
        return train, datasetCopy

    def convertStringColumnToFloat(self, hd, column):
        for row in hd:
            row[column] = float(row[column].strip()) 

    def convertStringColumnToInt(self, dataset, column):
        classValues = [row[column] for row in dataset]
        uniqueValues = set(classValues)
        lookup = dict()
        for i, value in enumerate(uniqueValues):
            lookup[value] = i
        for row in dataset:
            row[column] = lookup[row[column]]
        return lookup 

    def accuracyMetric(self, actual, predicted):
        correct = 0
        for i in range(len(actual)):
            if actual[i] == predicted[i]:
                correct += 1
        return correct / float(len(actual)) * 100.0

    def dataPreprocessing(self, filename):
        data = loadCsv(filename)
        hd = data[1: len(data)]
        for i in range(len(hd[0])-1):
            self.convertStringColumnToFloat(hd, i)
        self.convertStringColumnToInt(hd, len(hd[0])-1)
        dataTrain, dataTest = self.trainTestSplit(hd)
        return dataTrain, dataTest

    def perceptronModel(self, dataTrain, dataTest, patientCondition, actualResults):
        lRate = 0.06
        nEpoch = 1000 
        perceptronPredictions, patientDiagnosis = Perceptron.buildPerceptron(dataTrain, dataTest, patientCondition, lRate, nEpoch)
        perceptronAccuracy = self.perceptronEvaluation(perceptronPredictions, actualResults)
        return perceptronAccuracy, patientDiagnosis

    def knnModel(self, dataTrain, dataTest, patientCondition, actualResults):
        knnPredicts = list()
        for i in range(len(dataTest)):
            knnPrediction = KNN.buildKnn(dataTrain, dataTest[i], 4)
            knnPredicts.append(knnPrediction)
        knnAccuracy = self.accuracyMetric(actualResults, knnPredicts)
        patientDiagnosis = KNN.buildKnn(dataTrain, patientCondition, 4)
        return knnAccuracy, patientDiagnosis

    def perceptronEvaluation(self, perceptronPredictions, actualResults):
        intValsPerceptonPrecitions = list()
        for i in perceptronPredictions:
            intValsPerceptonPrecitions.append(int(i))
        perceptronAccuracy = self.accuracyMetric(actualResults, intValsPerceptonPrecitions)
        return perceptronAccuracy

    # take a look closely at how each row is being handled by the models
    def heartDiseaseDiagnosis(self, patient_conditions):
        trainDataset, testDataset = self.dataPreprocessing("clevelandV4.csv")
        test = testDataset[len(testDataset)-1]
        #realValue = patientCondition[-1]
        print("Y: {0}".format(test))
        print("X: {0}".format(patientConditions))
        actualResults = list()
        for row in testDataset:
            actualResults.append(row[-1])
        perceptronAccuracy, patientDiagnosisPerceptron = self.perceptronModel(trainDataset, testDataset, patient_conditions, actualResults)
        knnAccuracy, patientDiagnosisKNN = self.knnModel(trainDataset, testDataset, patient_conditions, actualResults)
        return perceptronAccuracy, patientDiagnosisPerceptron, knnAccuracy, patientDiagnosisKNN, 
