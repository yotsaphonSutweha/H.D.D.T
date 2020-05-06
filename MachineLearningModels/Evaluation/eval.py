import sys
sys.path.insert(1, './../')
import ml_ops

condition = [57,1,4,130,131,0,0,115,1,1.2,2,1,1]
actual_diagnosis = 1
eval_results = []
import csv

perceptron_correct = 'No'
knn_correct = 'No'
svm_correct = 'No'

for i in range(0, 100):
    perceptronAcc, patientDiagnosisPerceptron, knnAcc, patientdiagnosisKNN, svmAcc, patientDiagnosisSvm = ml_ops.heartDiseaseDiagnosis(condition)

    if int(patientDiagnosisPerceptron) == actual_diagnosis:
        perceptron_correct = 'Yes'
    
    if patientdiagnosisKNN == actual_diagnosis:
        knn_correct = 'Yes'
    
    if patientDiagnosisSvm == actual_diagnosis:
        svm_correct = 'Yes'

    tmp = [round(perceptronAcc, 2), patientDiagnosisPerceptron, round(knnAcc, 2), patientdiagnosisKNN, round(svmAcc, 2), patientDiagnosisSvm, perceptron_correct, knn_correct, svm_correct, actual_diagnosis]

    eval_results.append(tmp)

    perceptron_correct = 'No'
    knn_correct = 'No'
    svm_correct = 'No'

    print('Perceptron acc: {0}, Perceptron prediction: {1}, KNNAcc: {2}, KNNPrediction: {3}, SVM acc: {4}, SVM Prediction {5}'.format(perceptronAcc, patientDiagnosisPerceptron, knnAcc, patientdiagnosisKNN, svmAcc, patientDiagnosisSvm))

f = open('Models Evaluation Results.csv', 'w')
with f:
    writer = csv.writer(f)
    writer.writerow(["Perceptron Accuracy", "Perceptron Prediction", "KNN Accuracy", "KNN Prediction", "SVM Accuracy", "SVM Prediction", "Perceptron correct", "KNN correct", "SVM correct", "Actual Prediction"])
    for row in eval_results:
        writer.writerow(row)

