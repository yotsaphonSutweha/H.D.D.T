class ControllersHelper:
    
    def __init__(self):
        super().__init__()

    def check_int_value(self, value):
        try:
            if int(value):
                return True
        except:
            return False

    def prepare_patient_conditions(self, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
        patient_conditions = [float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), float(ca), float(thal)]
        return patient_conditions

    def determine_highest_accuracy_and_prediction(self, perceptron_accuracy, knn_accuracy, perceptron_predicted, knn_predicted):
        final_prediction = 0
        highest_accuracy = 0
        if perceptron_accuracy > knn_accuracy:
            final_prediction = perceptron_predicted
            highest_accuracy = perceptron_accuracy
        elif perceptron_accuracy < knn_accuracy:
            final_prediction = knn_predicted
            highest_accuracy = knn_accuracy
        return final_prediction, highest_accuracy

    def payload_preparation(self, perceptron_accuracy, perceptron_predicted, knn_accuracy, knn_predicted):
        models_details = {
                'perceptron' : {
                'name' : 'Perceptron',
                'accuracy' : perceptron_accuracy,
                'prediction' : perceptron_predicted
            },
                'knn' : {
                'name' : "K-nearest neighbours",
                'accuracy' : knn_accuracy,
                'prediction' : knn_predicted
            }
        }
        return models_details

    def prepare_medical_data_dictionary(self, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, final_prediction):
        medical_data = {
            'age' : age,
            'sex': sex,
            'cp': cp,
            'trestbps': trestbps,
            'chol': chol,
            'fbs': fbs,
            'restecg': restecg,
            'thalach': thalach,
            'exang': exang,
            'oldpeak': oldpeak,
            'slope': slope,
            'ca': ca,
            'thal': thal,
            'diagnosis': final_prediction
        }
        return medical_data

    def prepare_data_payload_for_ui_display(self, first_name, second_name, highest_accuracy, medical_data, models_details):
        personal_details = {
            'first_name' : first_name,
            'second_name' : second_name
        }
        data = {
            'accuracy' : highest_accuracy,
            'medical_details' : medical_data,
            'personal_details' : personal_details,
            'models_details' : models_details
        }
        return data
