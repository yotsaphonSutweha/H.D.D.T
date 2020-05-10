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
from Controllers.controllers_helper import ControllersHelper
diagnosis_controller = Blueprint('diagnosis_controller', __name__)
ops = Operations()
helpers = ControllersHelper()

# This is the diagnosis endpoint built by using Flask blueprints. It accepts the POST HTTP client method and has several CORS configurations attached to it.

# The diagnosis endpoint implementation:
# Step 1: check if the request is POST
# Step 2: check if the user session exists
# Step 3: check the user's access to the funtionality
# Step 4: get the patient's data from the request 
# Step 5: validates the user's request data
# Step 6: Execute the heart disease diagnosis using machine learing models
# Step 7: if everything pass, the endpoint should return the response with diagnostic result. Otherwise, the error message will be sent instead.

@diagnosis_controller.route('/api/diagnosis', methods=['POST'])
@cross_origin(origins='*', methods='POST', supports_credentials='true')
def diagnosis():
    if request.method == 'POST':
        if 'employeeId' in session:
            logged_in_user_id = session['employeeId']
            print(logged_in_user_id)
            doctor = ops.get_doctor_based_on_doctor_id(logged_in_user_id)
            nurse = ops.get_nurse_based_on_nurse_id(logged_in_user_id)
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
                print(type(age), sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
                if helpers.check_drop_down_values(sex, exang, fbs, oldpeak, restecg, ca, slope, thal, cp):
                    error_message = {
                        'message': 'Please choose appropriate medical data option in the drop down(s).'
                    }
                    return json_response(status_= 400, data_ = error_message)
                else:   
                    if helpers.check_int_value(age) and helpers.check_int_value(chol) and helpers.check_int_value(thalach) and helpers.check_int_value(trestbps) and helpers.check_information_length(first_name, second_name, address, contact_number, next_of_kin1_first_name, next_of_kin1_second_name, next_of_kin2_first_name, next_of_kin2_second_name):
                        # pass values to machine learning models
                        diagnostic_result = ''
                        perceptron_predicted_text = ''
                        knn_predicted_text = ''
                        final_prediction = 0
                        highest_accuracy = 0
                    
                        patient_conditions = helpers.prepare_patient_conditions(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
                    
                        # get the diagnosit result
                        perceptron_accuracy, perceptron_predicted, knn_accuracy, knn_predicted, svm_accuracy, svm_predicted = ml_ops.heartDiseaseDiagnosis(patient_conditions)

                        perceptron_accuracy = round(perceptron_accuracy, 2)
                        knn_accuracy = round(knn_accuracy, 2)
                        svm_accuracy = round(svm_accuracy, 2)

                        print("Perceptron accuracy {0} and {1}".format(perceptron_accuracy, perceptron_predicted))
                        print("KNN accuracy {0} and {1}".format(knn_accuracy, knn_predicted))
                        print("SVM accuracy {0} and {1}".format(svm_accuracy, svm_predicted))
                    
                        final_prediction, highest_accuracy = helpers.determine_highest_accuracy_and_prediction(perceptron_accuracy, knn_accuracy, perceptron_predicted, knn_predicted, svm_accuracy, svm_predicted)

                        # get the doctor based on Id
                        doctor = ops.get_doctor_based_on_doctor_id(logged_in_user_id)

                        # Perceptron details payload and Knn details payload
                        models_details = helpers.payload_preparation(perceptron_accuracy, perceptron_predicted, knn_accuracy, knn_predicted, svm_accuracy, svm_predicted)

                        # save the values to the database
                        medical_data = helpers.prepare_medical_data_dictionary(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, final_prediction)
                        severity = '0'

                        # Get the name of the doctor 
                        assigned_doctor_name = doctor.first_name + " " + doctor.second_name

                        print("Doctor's name {0}".format(assigned_doctor_name))

                        # Add patient's data to the database
                        ops.add_patient(
                            doctor,
                            first_name,
                            second_name,
                            address,
                            contact_number,
                            assigned_doctor_name,
                            next_of_kin1_first_name,
                            next_of_kin1_second_name,
                            next_of_kin2_first_name,
                            next_of_kin2_second_name,
                            severity,
                            medical_data
                        )

                        data = helpers.prepare_data_payload_for_ui_display(first_name, second_name, highest_accuracy, medical_data, models_details)

                        return json_response(data_ = data)
                    else:
                        error_message = {
                            'message': 'Please provide an appropriate information.'
                        }
                        return json_response(status_= 400, data_ = error_message)
            else:
                error_message = {
                    'message': 'You do not have access to this functionality.'
                }
                return json_response(status_= 403, data_ = error_message)
        else:
            error_message = {
                'message' : 'Please log in.'
            }
            return json_response(status_=400, data_ = error_message)
