from Database import createTables, createDatabase
from flask import flash

connection = createDatabase()
createTables()
cursor = connection.cursor()

def add_doctor(name, age, gender, specialization, current_status):
    cursor.execute('''INSERT INTO doctors (name, age, gender, specialization, current_status)
                   VALUES(?, ?, ?, ?, ?)''', (name, age, gender, specialization, current_status))
    connection.commit()
    id = cursor.lastrowid
    return id

def edit_doctor(doctor_id, name = None, age = None, gender = None, specialization = None, current_status = None):

    if name:
        cursor.execute("UPDATE doctors SET name = ? WHERE id = ?", (name, doctor_id))
    if age:
        cursor.execute("UPDATE doctors SET age = ? WHERE id = ?", (age, doctor_id))
    if gender:
        cursor.execute("UPDATE doctors SET gender = ? WHERE id = ?", (gender, doctor_id))
    if specialization:
        cursor.execute("UPDATE doctors SET specialization = ? WHERE id = ?", (specialization, doctor_id))
    if current_status:
        cursor.execute("UPDATE doctors SET current_status = ? WHERE id = ?", (current_status, doctor_id))
    connection.commit()

def delete_doctor(doctor_id):
    cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    connection.commit()

def search_doctor_by_id(id):
    cursor.execute("SELECT * FROM doctors WHERE id = ?", (id,))
    doctor = cursor.fetchone()
    return doctor

def search_doctors_by_name(name):
    cursor.execute("SELECT * FROM doctors WHERE name LIKE ?", (f"%{name}%",))
    doctors = cursor.fetchall()
    return doctors

def search_doctors_by_specialization(specialization):
    cursor.execute("SELECT * FROM doctors WHERE specialization LIKE ?", (f"%{specialization}%",))
    doctors = cursor.fetchall()
    return doctors

def search_doctors_by_current_status(current_status):
    cursor.execute("SELECT * FROM doctors WHERE current_status = ?", (current_status,))
    doctors = cursor.fetchall()
    return doctors

def view_all_doctors():
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    return doctors

def doctor_exists(doctor_id):
    cursor.execute("SELECT 1 FROM doctors WHERE id = ?", (doctor_id,))
    if cursor.fetchone() is None:
        flash(f"Doctor with ID {doctor_id} does not exist.", "error")
        return False
    return True


    

    
    