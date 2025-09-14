from Database import createDatabase
from flask import flash

connection = createDatabase()
cursor = connection.cursor()

def book_appointment(patient_id, doctor_id, room_no, dateAndTime):
    cursor.execute('''INSERT INTO appointments (patient_id, doctor_id, room_no, dateAndTime)
                   VALUES(?, ?, ?, ?)''', (patient_id, doctor_id, room_no, dateAndTime))
    connection.commit()
    id = cursor.lastrowid
    return id

def reschedule_appointment(appointment_id, doctor_id = None, room_no = None, newDateAndTime = None):
    if doctor_id:
        cursor.execute("UPDATE appointments SET doctor_id = ? WHERE id = ?", (doctor_id, appointment_id))
    if room_no:
        cursor.execute("UPDATE appointments SET room_no = ? WHERE id = ?", (room_no, appointment_id))
    if newDateAndTime:
        cursor.execute("UPDATE appointments SET dateAndTime = ? WHERE id = ?", (newDateAndTime, appointment_id))
    
    connection.commit()

def cancel_appointment(appointment_id):
    cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    connection.commit()

def view_all_appointments():
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    return appointments

def search_appointment_by_id(appointment_id):
    cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    appointment = cursor.fetchone()
    return appointment

def search_appointments_by_patientId(patient_id):
    cursor.execute("SELECT * FROM appointments WHERE patient_id = ?", (patient_id,))
    appointments = cursor.fetchall()
    return appointments

def search_appointments_by_doctorId(doctor_id):
    cursor.execute("SELECT * FROM appointments WHERE doctor_id = ?", (doctor_id,))
    appointments = cursor.fetchall()
    return appointments

def search_appointments_by_dateAndTime(dateAndTime):
    cursor.execute("SELECT * FROM appointments WHERE dateAndTime = ?", (dateAndTime,))
    appointments = cursor.fetchall()
    return appointments

def appointment_booked(appointment_id):
    cursor.execute("SELECT 1 FROM appointments WHERE id = ?", (appointment_id,))
    if cursor.fetchone() is None:
        flash(f"Appointment with ID {appointment_id} does not exist.", "error")
        return False
    return True
