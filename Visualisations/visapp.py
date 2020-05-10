import matplotlib
matplotlib.use('agg')
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import os
import pandas as pd
import io

# This class is used for generating the visualisation using Seaborn and matplot lib.
class Visualisations:
    def __init__(self):
        self.col1_name = ''
        self.col2_name = ''
        self.col1_value = ''
        self.col2_value = ''
        self.diagnosis_value = ''
        self.patient_data = None
        self.fig = None
        self.ax = None
        self.heart_disease_data = None

    # This method generates the scatter plot by using the user's selected values and the heart disease dataset. The output is in the form of bytes image.
    def generate_scatter_plot(self, col1_name, col2_name, col1_value, col2_value, diagnosis_value):

        self.col1_name = col1_name
        self.col2_name = col2_name
        self.col1_value = col1_value
        self.col2_value = col2_value
        self.diagnosis_value = diagnosis_value


        self.fig, self.ax = self.prepare_plot()

        self.heart_disease_data = self.load_heart_disease_dataset()

        pdata = {self.col1_name: [self.col1_value], self.col2_name: [ self.col2_value ], 'Patient diagnosis': [self.diagnosis_value]}

        self.patient_data = pd.DataFrame(data=pdata)

        sns.scatterplot(x=self.col1_name, y=self.col2_name, hue ='diagnosis', style='diagnosis', data = self.heart_disease_data, ax=self.ax)

        sns.scatterplot(x=self.col1_name, y=self.col2_name, hue='Patient diagnosis', alpha=0.6, data=self.patient_data, palette=['green'], ax=self.ax)     
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)

        return bytes_image
    
    # Prepare the plot.
    def prepare_plot(self):
        fig, ax = plt.subplots(figsize=(6, 5))
        return fig, ax

    # Load the dataset to be used with the visualisation.
    def load_heart_disease_dataset(self):
        here = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(here, '../MachineLearningModels/data/cleavelandAndHungarianData.csv')
        data = self.load_csv(filename)
        return data

    # Use pandas library to load the csv file.
    def load_csv(self, filename):
        dataset = pd.read_csv(filename)
        return dataset
