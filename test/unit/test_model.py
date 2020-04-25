import sys
sys.path.insert(1, './../../Models')
from operations import Operations
from schemas import Doctor
import os

class TestModelsOperations:
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.ops = Operations()
        cls.doctor_employeeId = "yo111"
        cls.nurse_employeeId = "yo112"
        cls.password = "12345678a"
        cls.first_name = "yotsaphon"
        cls.second_name = "sutweha"
        cls.contact_number = "0868441277"
        cls.room = "d1"
        cls.ward = "north1"
        cls.patient_first_name = "yo"
        cls.patient_second_name = "suts"
        cls.address = "54 Middle Abbey Street Dublin1"
        cls.contact_number = "0860234455"
        cls.assigned_doctor_name = "yotsaphon sutweha"
        cls.next_of_kin1_first_name = "yo"
        cls.next_of_kin1_second_name = "suts"
        cls.next_of_kin2_first_name = "yo"
        cls.next_of_kin2_second_name = "suts"
        cls.severity = "1"
        cls.medical_data = {}
        cls.new_patient_first_name = "aof"
        cls.new_patient_second_name = "don"
        cls.new_address = "55 Middle Abbey Street Dublin1"
        cls.new_contact_number = "0860234422"
        cls.new_next_of_kin1_first_name = "yotsaphon"
        cls.new_next_of_kin1_second_name = "sutweha"
        cls.new_next_of_kin2_first_name = "yotsaphon"
        cls.new_next_of_kin2_second_name = "sutweha"
        if cls.ops.check_the_doctor_collection_size() > 0:
            cls.ops.delete_doctor_collection()
        if cls.ops.check_the_patients_collection_size() > 0:
            cls.ops.delete_patients_collection()
        if cls.ops.check_the_nurse_collection_size() > 0:
            cls.ops.delete_nurse_collection()


    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        cls.doctor_employeeId = ""
        cls.nurse_employeeId = ""
        cls.password = ""
        cls.first_name = ""
        cls.second_name = ""
        cls.contact_number = ""
        cls.room = ""
        cls.ward = ""
        cls.patient_first_name = ""
        cls.patient_second_name = ""
        cls.address = ""
        cls.contact_number = ""
        cls.assigned_doctor_name = ""
        cls.next_of_kin1_first_name = ""
        cls.next_of_kin1_second_name = ""
        cls.next_of_kin2_first_name = ""
        cls.next_of_kin2_second_name = ""
        cls.severity = ""
        cls.medical_data = {}
        if cls.ops.check_the_doctor_collection_size() > 0:
            cls.ops.delete_doctor_collection()
        if cls.ops.check_the_patients_collection_size() > 0:
            cls.ops.delete_patients_collection()
        if cls.ops.check_the_nurse_collection_size() > 0:
            cls.ops.delete_nurse_collection()
        cls.ops = None
    
    def test_register_doctor(self):
        self.ops.register_doctor(self.doctor_employeeId, self.password, self.first_name, self.second_name, self.contact_number, self.room, self.ward)

        expected_result = 1
        actual_result = self.ops.check_the_doctor_collection_size()

        assert expected_result == actual_result

    def test_register_nurse(self):
        self.ops.register_nurse(self.nurse_employeeId, self.password, self.first_name, self.second_name, self.contact_number, self.room, self.ward)

        expected_result = 1
        actual_result = self.ops.check_the_nurse_collection_size()

        assert expected_result == actual_result

    def test_check_if_doctor_exists(self):
        expected_result = True
        acutal_result = self.ops.check_if_doctor_exist(self.doctor_employeeId)
        assert expected_result == acutal_result

    
    def test_check_if_nurse_exists(self):
        expected_result = True
        acutal_result = self.ops.check_if_nurse_exist(self.nurse_employeeId)
        assert expected_result == acutal_result

    def test_add_patient(self):
        doctor = self.ops.get_doctor_based_on_doctor_id(self.doctor_employeeId)

        self.ops.add_patient(doctor, self.patient_first_name, self.patient_second_name, self.address, self.contact_number, self.assigned_doctor_name, self.next_of_kin1_first_name, self.next_of_kin1_second_name, self.next_of_kin2_first_name, self.next_of_kin2_second_name, self.severity, self.medical_data)

        expected_result = 1
        actual_result = self.ops.check_the_patients_collection_size()
        assert expected_result == actual_result

    def test_get_every_patient(self):
        expected_result = 1
        actual_result = len(self.ops.get_every_patients())
        assert expected_result == actual_result

    def test_get_patients_based_on_doctor(self):
        doctor = self.ops.get_doctor_based_on_doctor_id(self.doctor_employeeId)
        expected_result = 1
        actual_result = len(self.ops.get_patients_based_on_doctor(doctor))
        assert expected_result == actual_result
    
    def test_get_patients_with_severity(self):
        expected_result = 1
        actual_result = len(self.ops.get_patients_with_severity())
        assert expected_result == actual_result

    def test_get_patient_based_on_patient_id(self):
        doctor = self.ops.get_doctor_based_on_doctor_id(self.doctor_employeeId)
        patient = self.ops.get_patients_based_on_doctor(doctor)
        expected_result = patient[0]['_id']['$oid']
        actual_result = self.ops.get_patient_based_on_patient_id(patient[0]['_id']['$oid'])['_id']['$oid']
        assert expected_result == actual_result

    def test_assigned_severity(self):
        doctor = self.ops.get_doctor_based_on_doctor_id(self.doctor_employeeId)
        patient = self.ops.get_patients_based_on_doctor(doctor)[0]
        new_severity = 5
        self.ops.assign_severity(patient['_id']['$oid'], new_severity)
        expected_result = 5
        actual_result = self.ops.get_patient_based_on_patient_id(patient['_id']['$oid'])['severity']
        assert expected_result == actual_result

    def test_update_patient_details(self):
        doctor = self.ops.get_doctor_based_on_doctor_id(self.doctor_employeeId)
        patient_id = self.ops.get_patients_based_on_doctor(doctor)[0]['_id']['$oid']
        self.ops.update_patient_details(patient_id, self.new_patient_first_name, self.new_patient_second_name, self.new_address, self.new_contact_number, self.new_next_of_kin1_first_name, self.new_next_of_kin1_second_name, self.new_next_of_kin2_first_name, self.new_next_of_kin2_second_name)

        expected_result = "aof"
        actual_result = self.ops.get_patient_based_on_patient_id(patient_id)['first_name']

        assert expected_result == actual_result

    def test_delete_patient(self):
        doctor = self.ops.get_doctor_based_on_doctor_id(self.doctor_employeeId)
        patient = self.ops.get_patients_based_on_doctor(doctor)[0]
        self.ops.delete_patient(patient['_id']['$oid'])
        expected_result = 0
        actual_result = len(self.ops.get_every_patients())
        assert expected_result == actual_result
   
