from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
import bcrypt
from flask import render_template, request, url_for, session, redirect
import MachineLearningModels.ml_ops as ml_ops
from flask_cors import cross_origin, CORS
from flask_json import as_json, json_response
diagnosis_controller = Blueprint('diagnosis_controller', __name__)
ops = Operations()

@diagnosis_controller.route('/api/diagnosis', methods=['POST'])
@cross_origin(origins='*', methods='POST', supports_credentials='true')
def diagnosis():
    if request.method == 'POST':
        if 'employeeId' in session:
            logged_in_user_id = session['employeeId']
            print(logged_in_user_id)
            doctor = ops.get_doctor_based_on_doctor_id(logged_in_user_id)
            if doctor != None and doctor.access_rights['diagnosis'] == True:
                first_name = request.json.get('first_name')
                second_name = request.json.get('second_name')
                address = request.json.get('address')
                contact_number = request.json.get('contact_number')
                next_of_kin1_first_name = request.json.get('next_of_kin1_first_name')
                next_of_kin1_second_name = request.json.get('next_of_kin1_second_name')
                next_of_kin2_first_name = request.json.get('next_of_kin2_first_name')
                next_of_kin2_second_name = request.json.get('next_of_kin2_second_name')
                print(first_name, second_name, address, contact_number, next_of_kin1_first_name, next_of_kin1_second_name, next_of_kin2_first_name, next_of_kin2_second_name)
                age = request.json.get('age')
                sex = request.json.get('gender')
                cp = request.json.get('cp')
                trestbps = request.json.get('trestbps')
                chol = request.json.get('chol')
                fbs = request.json.get('fbs')
                restecg = request.json.get('restecg')
                thalach = request.json.get('thalach')
                exang = request.json.get('exang')
                oldpeak = request.json.get('oldpeak')
                slope = request.json.get('slope')
                ca = request.json.get('ca')
                thal = request.json.get('thal')
                print(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)

                # pass values to machine learning models
                diagnostic_result = ''
                perceptron_predicted_text = ''
                knn_predicted_text = ''
                final_prediction = 0
                highest_accuracy = 0
                final_prediction_text = ''

                patient_conditions = [float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), float(ca), float(thal)]
               

                # get the diagnosit result
                perceptron_accuracy, perceptron_predicted, knn_accuracy, knn_predicted = ml_ops.heartDiseaseDiagnosis(patient_conditions)
                perceptron_accuracy = round(perceptron_accuracy, 2)
                knn_accuracy = round(knn_accuracy, 2)
             
                if perceptron_accuracy > knn_accuracy:
                    final_prediction = perceptron_predicted
                    highest_accuracy = perceptron_accuracy
                elif perceptron_accuracy < knn_accuracy:
                    final_prediction = knn_predicted
                    highest_accuracy = knn_accuracy
                # get the doctor based on Id
                doctor = ops.get_doctor_based_on_doctor_id(logged_in_user_id)

                if final_prediction == 0:
                    final_prediction_text = 'Diagnosed'
                elif final_prediction == 1:
                    final_prediction_text = 'Undiagnosed'

                # save the values to the database
                medical_data = {
                    "age" : age,
                    "sex": sex,
                    "cp": cp,
                    "trestbps": trestbps,
                    "chol": chol,
                    "fbs": fbs,
                    "restecg": restecg,
                    "thalach": thalach,
                    "exang": exang,
                    "oldpeak": oldpeak,
                    "slope": slope,
                    "ca": ca,
                    "thal": thal,
                    "diagnosis": final_prediction_text
                }
                severity = '0'


                ops.add_patient(
                    doctor,
                    first_name,
                    second_name,
                    address,
                    contact_number,
                    next_of_kin1_first_name,
                    next_of_kin1_second_name,
                    next_of_kin2_first_name,
                    next_of_kin2_second_name,
                    severity,
                    medical_data
                )

                data = {
                    'prediction' : final_prediction_text,
                    'accuracy' : highest_accuracy
                }

                # display the diagnostic result to the doctor
                return json_response(data_ = data)
            else:
                error_message = {
                    'message': 'You do not have access to this functionality'
                }
                return json_response(status_=403, data_ = error_message)
        else:
            error_message = {
                'message' : 'Please log in'
            }
            return json_response(status_=401, data_ = error_message)
   