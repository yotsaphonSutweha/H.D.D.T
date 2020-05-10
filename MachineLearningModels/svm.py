from sklearn.svm import SVC
class SVM:
    
    # This class contains support vector machine model implementation for testing, training and make prediction. Also, initialising the model object from the sci-kit learn library.

    def __init__(self):
        self.svm_model = SVC(C=30)

    def train(self, X_train, y_train):
        self.svm_model.fit(X_train, y_train)

    def test(self, X_test, y_test):
        return self.svm_model.score(X_test, y_test)
    
    def predict(self, patient_conditions):
        return self.svm_model.predict(patient_conditions)

    