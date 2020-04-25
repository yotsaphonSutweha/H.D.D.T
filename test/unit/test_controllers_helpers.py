import sys
sys.path.insert(1, './../../Controllers')
from controllers_helper import ControllersHelper
from random import choice
from string import ascii_lowercase

class TestControllersHelpers:
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.helpers = ControllersHelper()
        cls.int_value = 1
        cls.float_value = 1.0
        cls.accuracy = 97
        cls.predicted = 1
        cls.personal_details = {
            'first_name' : 'Yo',
            'second_name' : 'Suts'
        }
        cls.medical_details = {
            'test': 'this is a test'
        }
        cls.models_details = {
            'test' : 'this is a test'
        }
        cls.patient_first_name = 'yo'
        cls.patient_second_name = 'suts'
        cls.address = '54 Middle Abbey Street Dublin1'
        cls.contact_number = '0860234455'
        cls.next_of_kin1_first_name = 'yo'
        cls.next_of_kin1_second_name = 'suts'
        cls.next_of_kin2_first_name = 'yo'
        cls.next_of_kin2_second_name = 'suts'
        cls.choose = 'Choose...'
        cls.perceptron_predicted = 1
        cls.svm_predicted = 1
        cls.knn_predicted = 0
        cls.svm_accuracy = 80
        cls.knn_accuracy = 50
        cls.one_hundred_string_length = ''.join(choice(ascii_lowercase) for i in range(102))
        cls.bad_contact_number = '0860234455aaa'
        cls.gender_str = 'gender'
        cls.fbs_str = 'fbs'
        
    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        cls.helpers = None
        cls.int_value = None
        cls.float_value = None
        cls.accuracy = None
        cls.predicted = None
        cls.personal_details = None
        cls.medical_details = None
        cls.models_details = None
        cls.patient_first_name = None
        cls.patient_second_name = None
        cls.address = None
        cls.contact_number = None
        cls.next_of_kin1_first_name = None
        cls.next_of_kin1_second_name = None
        cls.next_of_kin2_first_name = None
        cls.next_of_kin2_second_name = None
        cls.choose = None
        cls.perceptron_predicted = None
        cls.svm_predicted = None
        cls.knn_predicted = None
        cls.svm_accuracy = None
        cls.knn_accuracy = None
        cls.one_hundred_string_length = None
        cls.bad_contact_number = None
        cls.gender_str = None
        cls.fbs_str = None

    # Happy paths
    def test_check_int_value_true(self):
        expected_result = True
        actual_result = self.helpers.check_int_value(self.int_value)
        assert expected_result == actual_result

    def test_prepare_patient_conditions(self):
        expected_result = [self.float_value, self.float_value, self.float_value, self.float_value, self.float_value, self.float_value, self.float_value, self.float_value, self.float_value, self.float_value, self.float_value, self.float_value, self.float_value]
        actual_result = self.helpers.prepare_patient_conditions(self.int_value,self.int_value,self.int_value,self.int_value,self.int_value,self.int_value,self.int_value,self.int_value,self.int_value,self.int_value,self.int_value,self.int_value,self.int_value)
        assert expected_result == actual_result
    
    def test_payload_preparation(self):
        expected_result = {
            'perceptron' : {
                'name' : 'Perceptron',
                'accuracy' : self.accuracy,
                'prediction' : self.predicted
            },
            'knn' : {
                'name' : 'K-nearest neighbours',
                'accuracy' : self.accuracy,
                'prediction' : self.predicted
            },
            'svm' : {
                'name': 'Support Vector Machine',
                'accuracy' : self.accuracy,
                'prediction' : self.predicted
            }
        }
        actual_result = self.helpers.payload_preparation(self.accuracy, self.predicted, self.accuracy, self.predicted, self.accuracy, self.predicted)

        assert expected_result == actual_result

    def test_prepare_medical_data_dictionary(self):
        expected_result = {
            'age' : self.int_value,
            'sex': self.int_value,
            'cp': self.int_value,
            'trestbps': self.int_value,
            'chol': self.int_value,
            'fbs': self.int_value,
            'restecg': self.int_value,
            'thalach': self.int_value,
            'exang': self.int_value,
            'oldpeak': self.int_value,
            'slope': self.int_value,
            'ca': self.int_value,
            'thal': self.int_value,
            'diagnosis': self.int_value
        }
        actual_result = self.helpers.prepare_medical_data_dictionary(self.int_value, self.int_value, self.int_value, self.int_value,self.int_value, self.int_value, self.int_value, self.int_value, self.int_value, self.int_value, self.int_value, self.int_value, self.int_value, self.int_value)

        assert expected_result == actual_result

    def test_prepare_data_payload_for_ui_display(self):
        expected_result = {
            'accuracy' : self.accuracy,
            'medical_details' : self.medical_details,
            'personal_details' : self.personal_details,
            'models_details' : self.models_details
        }
        actual_result = self.helpers.prepare_data_payload_for_ui_display(self.personal_details['first_name'], self.personal_details['second_name'], self.accuracy, self.medical_details, self.models_details)
        assert expected_result == actual_result

    def test_check_information_length_true(self):
        expected_result = True
        actual_result = self.helpers.check_information_length(self.patient_first_name, self.patient_second_name, self.address, self.contact_number, self.next_of_kin1_first_name, self.next_of_kin1_second_name,  self.next_of_kin2_first_name, self.next_of_kin2_second_name)
        assert expected_result == actual_result

    def test_check_contact_number_false(self):
        expected_result = False
        actual_result = self.helpers.check_contact_number(self.contact_number)
        assert expected_result == actual_result
    
    def test_check_drop_down_values_false(self):
        expected_result = False
        actual_result = self.helpers.check_drop_down_values(self.int_value, self.int_value,self.int_value, self.int_value, self.int_value, self.int_value, self.int_value, self.int_value, self.int_value)
        assert expected_result == actual_result

    def test_check_x_and_y_axis_name_false(self):
        expected_result = False
        actual_result = self.helpers.check_x_and_y_axis_name(self.gender_str, self.fbs_str, self.int_value, self.int_value)
        assert expected_result == actual_result

    def test_determine_highest_accuracy_and_prediction(self):
        expected_result = 1, 97
        actual_result = self.helpers.determine_highest_accuracy_and_prediction(self.accuracy, self.knn_accuracy, self.perceptron_predicted, self.knn_predicted, self.svm_accuracy, self.svm_predicted)
        assert expected_result == actual_result

    # Unhappy paths 
    def test_check_int_value_false(self):
        expected_result = False
        actual_result = self.helpers.check_int_value('')
        assert expected_result == actual_result

    def test_check_information_length_false(self):
        expected_result = False
        actual_result = self.helpers.check_information_length(self.one_hundred_string_length, self.one_hundred_string_length, self.one_hundred_string_length, self.bad_contact_number, self.one_hundred_string_length, self.one_hundred_string_length,  self.one_hundred_string_length, self.one_hundred_string_length)
        assert expected_result == actual_result
    
    def test_check_contact_number_true(self):
        expected_result = True
        actual_result = self.helpers.check_contact_number(self.bad_contact_number)
        assert expected_result == actual_result

    def test_check_drop_down_values_true(self):
        expected_result = True
        actual_result = self.helpers.check_drop_down_values(self.choose, self.choose,self.choose, self.choose, self.choose, self.choose, self.choose, self.choose, self.choose)
        assert expected_result == actual_result

    def test_check_x_and_y_axis_name_true(self):
        expected_result = True
        actual_result = self.helpers.check_x_and_y_axis_name(self.choose, self.choose, None, None)
        assert expected_result == actual_result