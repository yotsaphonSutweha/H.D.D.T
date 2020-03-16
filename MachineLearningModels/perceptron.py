class Perceptron:
    def __init__(self):
        super().__init__()

    def buildPerceptron(self, train, test, patientCondition, lRate, nEpoch):
        predictions = list()
        patientDiagnosis = -1
        prediction = 0
        weights = self.trainWeights(train, lRate, nEpoch)
        for row in test:
            prediction = self.predict(row, weights)
            predictions.append(prediction)
        return (predictions), weights

    def patientDiagnosis(self, patientCondition, weights):
        if patientCondition != None:
                patientDiagnosis = self.predict(patientCondition, weights)
        return patientDiagnosis

    def trainWeights(self, train, lRate, nEpoch):
        weights = [0.0 for i in range(len(train[0]))]
        for _ in range(nEpoch):
            for row in train:
                prediction = self.predict(row, weights)
                error = row[-1] - prediction
                weights[0] = weights[0] + lRate * error
                for i in range(len(row)-1):
                    weights[i+1] = weights[i+1] +lRate * error * row[i]
        return weights

    def predict(self, row, weights):
        activation = weights[0]
        for i in range(len(row) - 1):
            activation += weights[i+1] * row[i]
        return 1.0 if activation >= 0.0 else 0.0