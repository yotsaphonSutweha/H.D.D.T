import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class TestDiagnosingPatient:
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.driver = webdriver.Chrome('./chromedriver')
        cls.driver.implicitly_wait(1000)
        cls.driver.maximize_window()
        cls.first_name = 'tester'
        cls.second_name = 'tester'
        cls.contact_number = '0987765533'
        cls.address = '54 Middle Abbey Street, Dublin 1'
        cls.next_of_kin_name = 'tester'
        cls.age = '54'
        cls.gender = 'Male'
        cls.chol = '236'
        cls.thalach = '174'
        cls.exang = 'Yes'
        cls.fbs = 'Yes'
        cls.oldpeak = '2'
        cls.restecg = 'Normal'
        cls.ca = '2'
        cls.slope = 'Flat'
        cls.thal = 'Normal'
        cls.cp = 'Asymptotic'
        cls.trestbps = '130'
        cls.expected_first_name = 'First name: tester'
        cls.expected_second_name = 'Second name: tester'
        cls.expected_age = 'Age: 54'
        cls.expected_gender = 'Gender: Male'
        cls.expected_chol = 'Serum Cholestrol in mg/dl: 236'
        cls.expected_thalach = 'Maximum Heart Rate Achieved: 174'
        cls.expected_exang = 'Exercise Induced Agina: Yes'
        cls.expected_fbs = 'Fasting Blood Sugar (>120mg/dl): Yes'
        cls.expected_oldpeak = 'ST Depression Induced: 2'
        cls.expected_restecg = 'Resting Electrocardiographic Result: Normal'
        cls.expected_ca = 'Number of Major Vessels: 2'
        cls.expected_slope = 'Slope of Peak Exercise ST Segment: Flat'
        cls.expected_thal = 'Thalassemia: Normal'
        cls.expected_cp = 'Chest-pain Type: Asymptotic'
        cls.expected_trestbps = 'Resting Blood Pressure in mmHg: 130'
      
        
      
    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        ""
        cls.first_name = None
        cls.second_name = None
        cls.contact_number = None
        cls.address = None
        cls.next_of_kin_name = None
        cls.age = None
        cls.gender = None
        cls.chol = None
        cls.thalach = None
        cls.exang = None
        cls.fbs = None
        cls.oldpeak = None
        cls.restecg = None
        cls.ca = None
        cls.slope = None
        cls.thal = None
        cls.cp = None
        cls.trestbps = None
        cls.expected_first_name = None
        cls.expected_second_name = None
        cls.expected_age = None
        cls.expected_gender = None
        cls.expected_chol = None
        cls.expected_thalach = None
        cls.expected_exang = None
        cls.expected_fbs = None
        cls.expected_oldpeak = None
        cls.expected_restecg = None
        cls.expected_ca = None
        cls.expected_slope = None
        cls.expected_thal = None
        cls.expected_cp = None
        cls.expected_trestbps = None
        cls.driver.close()
        cls.driver = None
    
    def test_register(self):
        self.driver.get('http://localhost:3000/register')
        self.driver.find_element_by_name('employeeId').send_keys('tester01')
        self.driver.find_element_by_name('password').send_keys('tester1234567')
        Select(self.driver.find_element_by_name('jobRole')).select_by_visible_text('Doctor')
        self.driver.find_element_by_name('confirmPassword').send_keys('tester1234567')
        self.driver.find_element_by_name('firstName').send_keys('tester')
        self.driver.find_element_by_name('secondName').send_keys('tester')
        self.driver.find_element_by_name('contactNumber').send_keys('0897765544')
        self.driver.find_element_by_name('room').send_keys('098')
        self.driver.find_element_by_name('ward').send_keys('east')
        self.driver.find_element_by_class_name('button').click()

    def test_diagnosing_patient(self):
        # 1st step: log in to the application using the registered details
        self.driver.get('http://localhost:3000/login')
        self.driver.find_element_by_name('employeeId').send_keys('tester01')
        self.driver.find_element_by_name('password').send_keys('tester1234567')
        self.driver.find_element_by_class_name('button').click()

        # 2nd step: verify if logged in by checking the heading on the patients page
        assert 'Patients' == self.driver.find_element_by_class_name('heading').text

        # 3rd step: Go to the diagnose patient page and verify if the page is actually presented
        self.driver.get('http://localhost:3000/diagnose-patient')
        assert 'Diagnose Patient' == self.driver.find_element_by_class_name('heading').text

        # 4th step: Fill out personal details and medical details
        self.driver.find_element_by_name('firstName').send_keys(self.first_name)
        self.driver.find_element_by_name('secondName').send_keys(self.second_name)
        self.driver.find_element_by_name('contactNumber').send_keys(self.contact_number)
        self.driver.find_element_by_name('address').send_keys(self.address)
        self.driver.find_element_by_name('nextOfKin1FirstName').send_keys(self.next_of_kin_name)
        self.driver.find_element_by_name('nextOfKin1SecondName').send_keys(self.next_of_kin_name)
        self.driver.find_element_by_name('nextOfKin2FirstName').send_keys(self.next_of_kin_name)
        self.driver.find_element_by_name('nextOfKin2SecondName').send_keys(self.next_of_kin_name)
        self.driver.find_element_by_name('age').send_keys(self.age)
        Select(self.driver.find_element_by_name('gender')).select_by_visible_text(self.gender)
        self.driver.find_element_by_name('chol').send_keys(self.chol)
        self.driver.find_element_by_name('thalach').send_keys(self.thalach)
        Select(self.driver.find_element_by_name('exang')).select_by_visible_text(self.exang)
        Select(self.driver.find_element_by_name('fbs')).select_by_visible_text( self.fbs)
        Select(self.driver.find_element_by_name('oldpeak')).select_by_visible_text(self.oldpeak)
        Select(self.driver.find_element_by_name('restecg')).select_by_visible_text(self.restecg)
        Select(self.driver.find_element_by_name('ca')).select_by_visible_text(self.ca)
        Select(self.driver.find_element_by_name('slope')).select_by_visible_text(self.slope)
        Select(self.driver.find_element_by_name('thal')).select_by_visible_text(self.thal)
        Select(self.driver.find_element_by_name('cp')).select_by_visible_text(self.cp)
        self.driver.find_element_by_name('trestbps').send_keys(self.trestbps)

        # 5th step: Click on the diagnose button to initiate the diagnostic process
        self.driver.find_element_by_class_name('button').click()

        # Get the elements that are present on the diagnosis results page
        results_page_heading1 = self.driver.find_element_by_id('diagnosticAccuracy').text
        results_page_heading2 = self.driver.find_element_by_id('diagnosticResult').text
        personal_details_section = self.driver.find_element_by_id('personalInfoHeading').text
        medical_details_section = self.driver.find_element_by_id('medicalInfoHeading').text
        actual_first_name = self.driver.find_element_by_id('firstName').text
        actual_second_name = self.driver.find_element_by_id('secondName').text
        actual_age = self.driver.find_element_by_id('age').text
        actual_gender = self.driver.find_element_by_id('gender').text
        actual_chol = self.driver.find_element_by_id('chol').text
        actual_cp = self.driver.find_element_by_id('cp').text
        actual_exang = self.driver.find_element_by_id('exang').text
        actual_fbs = self.driver.find_element_by_id('fbs').text
        actual_oldpeak = self.driver.find_element_by_id('oldpeak').text
        actual_restecg =  self.driver.find_element_by_id('restecg').text
        actual_ca =  self.driver.find_element_by_id('ca').text
        actual_thal =  self.driver.find_element_by_id('thal').text
        actual_thalach =  self.driver.find_element_by_id('thalach').text
        actual_trestbps =  self.driver.find_element_by_id('trestbps').text
        actual_slope =  self.driver.find_element_by_id('slope').text
        models_table =  self.driver.find_element_by_id('mlModelsTable')


        # 6th: Verify if the actual results are correct as expected. This is to simulate if the user is getting the diganostic results from the machine learning models

        assert 'Diagnostic Accuracy' == results_page_heading1
        assert 'Diagnostic Result' == results_page_heading2
        assert 'Personal Information' == personal_details_section
        assert 'Medical Information' == medical_details_section
        assert models_table != None
        assert self.expected_first_name == actual_first_name
        assert self.expected_second_name == actual_second_name
        assert self.expected_age == actual_age
        assert self.expected_gender == actual_gender
        assert self.expected_chol == actual_chol
        assert self.expected_thalach == actual_thalach
        assert self.expected_exang == actual_exang
        assert self.expected_fbs == actual_fbs
        assert self.expected_oldpeak == actual_oldpeak
        assert self.expected_restecg == actual_restecg
        assert self.expected_ca == actual_ca
        assert self.expected_slope == actual_slope
        assert self.expected_thal == actual_thal
        assert self.expected_cp == actual_cp
        assert self.expected_trestbps == actual_trestbps

    def test_assign_severity(self):
        # 1st step: Log in to the application using the registered details
        self.driver.get('http://localhost:3000/login')
        self.driver.find_element_by_name('employeeId').send_keys('tester01')
        self.driver.find_element_by_name('password').send_keys('tester1234567')
        self.driver.find_element_by_class_name('button').click()

        # 2nd step: Verify if logged in by checking the heading on the patients page
        assert 'Patients' == self.driver.find_element_by_class_name('heading').text

        # 3rd step: Click on the view button
        self.driver.find_element_by_class_name('button').click()

        # 4th step: Click on visualise condition button
        self.driver.find_element_by_class_name('button').click()

        # 5th step: Select medical condictions and generate visualisation 
        Select(self.driver.find_element_by_id('condition1')).select_by_visible_text('Age')
        Select(self.driver.find_element_by_id('condition2')).select_by_visible_text('Serum Cholesterol')
        self.driver.find_element_by_id('generateButton').click()
        # 6th step: Assign severity 
        self.driver.find_element_by_name('severity').send_keys('5')
        self.driver.find_element_by_id('assignButton').click()
        # 7th step: Verify if the severity is assigned by using the alert
        expectedSuccessfulMsg = 'Severity has been assigned successfully! Patient is added to the operation awaiting list.'
        actualSuccessfulMsg = self.driver.find_element_by_class_name('alert-success').text[0:-2]
        assert expectedSuccessfulMsg == actualSuccessfulMsg

    def test_view_awaiting_list(self):
        # 1st step: Log in to the application using the registered details
        self.driver.get('http://localhost:3000/login')
        self.driver.find_element_by_name('employeeId').send_keys('tester01')
        self.driver.find_element_by_name('password').send_keys('tester1234567')
        self.driver.find_element_by_class_name('button').click()

        # 2nd step: Verify if logged in by checking the heading on the patients page
        assert 'Patients' == self.driver.find_element_by_class_name('heading').text

        # 3rd step: Go to the awaiting list page 
        self.driver.get('http://localhost:3000/waiting-list')

        # 4th step: Verify if the awaiting list page is presented
        assert 'Operation Awaiting List' == self.driver.find_element_by_class_name('heading').text
        

      
    

 