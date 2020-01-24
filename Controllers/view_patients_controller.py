from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
import bcrypt
from flask import render_template, request, url_for, session, redirect
import MachineLearningModels.ml_ops as ml_ops
view_patients_controller = Blueprint('view_patients_controller', __name__)
ops = Operations()