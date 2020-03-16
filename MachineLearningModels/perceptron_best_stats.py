class PerceptronStats:
    def __init__(self):
        self.bestWeights = []
        self.bestAccuracy = 0.0
    
    def set_weights(self, weights):
        self.bestWeights = weights
    
    def set_accuracy(self, accuracy):
        self.bestAccuracy = accuracy

    def get_weights(self):
        return self.bestWeights
    
    def get_accuracy(self):
        return self.bestAccuracy