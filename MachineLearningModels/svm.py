from sklearn.svm import SVC
class SVM:
    def __init__(self):
        self.svm_model = SVC(C=30)

    def train(self, X_train, y_train):
        self.svm_model.fit(X_train, y_train)

    def test(self, X_test, y_test):
        return self.svm_model.score(X_test, y_test)
    
    def predict(self, patient_condictions):
        return self.svm_model.predict(patient_condictions)

    