from Database import createTables, createDatabase
from flask import flash

connection = createDatabase()
cursor = connection.cursor()

def add_patient(name, age, gender, disease, medical_history):
    cursor.execute('''INSERT INTO patients (name, age, gender, disease, medical_history)
                   VALUES(?, ?, ?, ?, ?)''', (name, age, gender, disease, medical_history))
    connection.commit()
    id = cursor.lastrowid
    return id

def edit_patient(patient_id, name = None, age = None, gender = None, disease = None, medical_history = None):
    if name:
        cursor.execute("UPDATE patients SET name = ? WHERE id = ?", (name, patient_id))
    if age:
        cursor.execute("UPDATE patients SET age = ? WHERE id = ?", (age, patient_id))
    if gender:
        cursor.execute("UPDATE patients SET gender = ? WHERE id = ?", (gender, patient_id))
    if disease:
        cursor.execute("UPDATE patients SET disease = ? WHERE id = ?", (disease, patient_id))
    if medical_history:
        cursor.execute("UPDATE patients SET medical_history = ? WHERE id = ?", (medical_history, patient_id))
    
    connection.commit()

def delete_patient(patient_id):
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    connection.commit()

def search_patient_by_id(patient_id):
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    return patient

def search_patients_by_name(name):
    cursor.execute("SELECT * FROM patients WHERE name LIKE ?", (f"%{name}%",))
    patients = cursor.fetchall()
    return patients

def search_patients_by_disease(disease):
    cursor.execute("SELECT * FROM patients WHERE disease LIKE ?", (f"%{disease}%",))
    patients = cursor.fetchall()
    return patients
    

def view_all_patients():
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    return patients

def patient_exists(patient_id):
    cursor.execute("SELECT 1 FROM patients WHERE id = ?", (patient_id,))
    if cursor.fetchone() is None:
        flash(f"Patient with ID {patient_id} does not exist.", "error")
        return False
    return True