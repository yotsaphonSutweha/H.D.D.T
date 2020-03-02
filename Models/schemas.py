from Controllers.extensions import mongo
from datetime import datetime
import json

class Doctor(mongo.Document):
        doctor_id = mongo.StringField(required=True, unique=True)
        password = mongo.StringField(required=True)
        first_name = mongo.StringField(max_length=40)
        second_name = mongo.StringField(max_length=40)
        contact_number = mongo.StringField(max_length=13)
        room_number = mongo.StringField(max_length=3)
        ward = mongo.StringField(max_length=10)
        date_created = mongo.DateTimeField(default=datetime.utcnow)
        access_rights = mongo.DictField(mongo.BooleanField())

        def json(self):
            doctor_dict = {
                "doctor_id" : self.doctor_id,
                "password" : self.password,
                "first_name" : self.first_name,
                "second_name" : self.second_name,
                "contact_number" : self.contact_number,
                "room_number": self.room_number,
                "ward": self.ward,
                "date_created" : self.date_created,
                "access_rights" : self.access_rights
            }
            return json.dumps(doctor_dict)

        meta = {
            "indexes" : ["doctor_id", "second_name"],
            "ordering": ["-date_created"]
        }

class Patient(mongo.Document):
        assigned_doctor = mongo.ReferenceField(Doctor)
        first_name = mongo.StringField(max_length=40, required=True)
        second_name = mongo.StringField(max_length=40, required=True)
        address = mongo.StringField(max_length=100, required=True)
        contact_number = mongo.StringField(max_length=13, required=True)
        next_of_kin1_first_name =  mongo.StringField(max_length=40, required=True)
        next_of_kin1_second_name =  mongo.StringField(max_length=40, required=True)
        next_of_kin2_first_name =  mongo.StringField(max_length=40)
        next_of_kin2_second_name =  mongo.StringField(max_length=40)
        date_created = mongo.DateTimeField(default=datetime.utcnow)
        severity = mongo.IntField()
        medical_data = mongo.DictField()

        def json(self):
            patient_dict = {
                "assigned_doctor" : self.assigned_doctor,
                "first_name" : self.first_name,
                "second_name" : self.second_name,
                "address" : self.address,
                "contact_number" : self.contact_number,
                "next_of_kin1_first_name" : self.next_of_kin1_first_name,
                "next_of_kin1_second_name" : self.next_of_kin1_second_name,
                "next_of_kin2_first_name" : self.next_of_kin2_first_name,
                "next_of_kin2_second_name" : self.next_of_kin2_second_name,
                "severity" : self.severity,
                "medical_data" : self.medical_data
            }
            return json.dumps(patient_dict)

        meta = {
            "indexes" : ["first_name", "second_name", "assigned_doctor"],
            "ordering": ["-date_created"]
        }

class Nurse(mongo.Document):
        nurse_id = mongo.StringField(required=True, unique=True)
        password = mongo.StringField(required=True)
        first_name = mongo.StringField(max_length=40)
        second_name = mongo.StringField(max_length=40)
        contact_number = mongo.StringField(max_length=13)
        ward = mongo.StringField(max_length=10)
        date_created = mongo.DateTimeField(default=datetime.utcnow)
        access_rights = mongo.DictField(mongo.BooleanField())

        def json(self):
            doctor_dict = {
                "nurse_id" : self.doctor_id,
                "password" : self.password,
                "first_name" : self.first_name,
                "second_name" : self.second_name,
                "contact_number" : self.contact_number,
                "ward": self.ward,
                "date_created" : self.date_created,
                "access_rights" : self.access_rights
            }
            return json.dumps(doctor_dict)

        meta = {
            "indexes" : ["nurse_id", "second_name"],
            "ordering": ["-date_created"]
        }