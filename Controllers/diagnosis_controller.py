from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
import bcrypt
from flask import render_template, request, url_for, session, redirect
import MachineLearningModels.ml_ops as ml_ops
diagnosis_controller = Blueprint('diagnosis_controller', __name__)
ops = Operations()

@diagnosis_controller.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    if request.method == 'POST':
        if 'employeeId' in session:
            logged_in_user_id = session['employeeId']
            print(logged_in_user_id)
            doctor = ops.get_doctor_based_on_doctor_id(logged_in_user_id)
            if doctor != None and doctor.access_rights['diagnosis'] == True:
                first_name = request.form.get('first_name')
                second_name = request.form.get('second_name')
                address = request.form.get('address')
                contact_number = request.form.get('contact_number')
                next_of_kin1_first_name = request.form.get('next_of_kin1_first_name')
                next_of_kin1_second_name = request.form.get('next_of_kin1_second_name')
                next_of_kin2_first_name = request.form.get('next_of_kin2_first_name')
                next_of_kin2_second_name = request.form.get('next_of_kin2_second_name')
                print(first_name, second_name, address, contact_number, next_of_kin1_first_name, next_of_kin1_second_name, next_of_kin2_first_name, next_of_kin2_second_name)
                age = request.form.get('age')
                sex = request.form.get('sex')
                cp = request.form.get('cp')
                trestbps = request.form.get('trestbps')
                chol = request.form.get('chol')
                fbs = request.form.get('fbs')
                restecg = request.form.get('restecg')
                thalach = request.form.get('thalach')
                exang = request.form.get('exang')
                oldpeak = request.form.get('oldpeak')
                slope = request.form.get('slope')
                ca = request.form.get('ca')
                thal = request.form.get('thal')
                print(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)

                # pass values to machine learning models
                diagnostic_result = ''
                perceptron_predicted_text = ''
                knn_predicted_text = ''
                final_prediction = 0

                patient_conditions = [float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), float(ca), float(thal)]
               

                # get the diagnosit result
                perceptron_accuracy, perceptron_predicted, knn_accuracy, knn_predicted = ml_ops.heartDiseaseDiagnosis(patient_conditions)
                perceptron_accuracy = round(perceptron_accuracy, 2)
                knn_accuracy = round(knn_accuracy, 2)
                print(perceptron_accuracy)
                print(knn_accuracy)
                if perceptron_accuracy > knn_accuracy:
                    final_prediction = perceptron_predicted
                elif perceptron_accuracy < knn_accuracy:
                    final_prediction = knn_predicted

                # get the doctor based on Id
                doctor = ops.get_doctor_based_on_doctor_id(logged_in_user_id)

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
                    "diagnosis": final_prediction
                }
                severity = 1

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

                # display the diagnostic result to the doctor
                return '<h1>YES</h1>'
            else:
                return '<h1>You do not have access to this page</h1>'
        else:
            return '<h1>Please login</h1>'

    return render_template('diagnosis.html')