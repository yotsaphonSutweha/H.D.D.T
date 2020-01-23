class Perceptron:
    def __init__(self, name):
        self.name = name
        
    def buildPerceptron(train, test, patientCondition, lRate, nEpoch):
        predictions = list()
        patientDiagnosis = -1
        weights = trainWeights(train, lRate, nEpoch)
        for row in test:
            prediction = predict(row, weights)
            predictions.append(prediction)
        
        if patientCondition != None:
            patientDiagnosis = predict(patientCondition, weights)
        
        return (predictions), patientDiagnosis

    def trainWeights(train, lRate, nEpoch):
        weights = [0.0 for i in range(len(train[0]))]
        for _ in range(nEpoch):
            for row in train:
                prediction = predict(row, weights)
                error = row[-1] - prediction
                weights[0] = weights[0] + lRate * error
                for i in range(len(row)-1):
                    weights[i+1] = weights[i+1] +lRate * error * row[i]
        return weights

    def predict(row, weights):
        activition = weights[0]
        for i in range(len(row) - 1):
            activition += weights[i+1] * row[i]
        return 1.0 if activition >= 0.0 else 0.0