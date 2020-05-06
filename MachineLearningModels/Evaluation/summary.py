import pandas as pd
import os

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, './Models Evaluation Results.csv')
dataset = pd.read_csv(filename)

perceptronCorrects = dataset['Perceptron correct'].value_counts()['Yes']
perceptronWrongs = dataset['Perceptron correct'].value_counts()['No']
knnCorrects = dataset['KNN correct'].value_counts()['Yes']
knnWrongs = dataset['KNN correct'].value_counts()['No']
svmCorrects = dataset['SVM correct'].value_counts()['Yes']
svmWrongs = dataset['SVM correct'].value_counts()['No']

print('Perceptron Yes {0}, No {1}'.format(perceptronCorrects, perceptronWrongs))
print('KNN Yes {0}, No {1}'.format(knnCorrects, knnWrongs))
print('SVM Yes {0}, No {1}'.format(svmCorrects, svmWrongs))