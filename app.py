from flask import Flask, render_template, request, url_for, redirect, flash
from Doctor_Management import add_doctor, edit_doctor, delete_doctor, search_doctor_by_id, search_doctors_by_name, search_doctors_by_current_status, search_doctors_by_specialization, view_all_doctors, doctor_exists
from Patient_Management import add_patient, edit_patient, delete_patient, search_patient_by_id, search_patients_by_disease, search_patients_by_name, view_all_patients, patient_exists
from Appointment_Sceduling import book_appointment, reschedule_appointment, cancel_appointment, view_all_appointments, search_appointment_by_id, search_appointments_by_patientId, search_appointments_by_doctorId, search_appointments_by_dateAndTime, appointment_booked
from Billing_System import generate_invoice, edit_invoice, delete_invoice, apply_discount, search_invoice_by_id, search_invoices_by_patientId, view_all_invoices, invoice_generated
from Report import total_patients_treated_for_specific_timeframe, revenue_for_specific_timeframe, doctor_performance, full_report
from Database import createDatabase, createTables
import os
createDatabase()
createTables()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devsecret")
usernameinfo = "abcdefgh"
passwordinfo = "12345678"

@app.route("/", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == usernameinfo:
            if password == passwordinfo:
                return redirect(url_for("home"))
            else:
                flash("Incorrect Password!", "error")
                return redirect(url_for("login"))
        else:
            flash("Incorrect Username!", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/patient")
def patient_management():
    return render_template("patient_management.html")

@app.route("/patient/action", methods=["GET"])
def patient_action():
    action = request.args.get("action")
    print(action)

    if action == 'add':
        return redirect(url_for('add_patient1'))
    elif action == 'edit':
        return redirect(url_for('edit_patient1'))
    elif action == 'delete':
        return redirect(url_for('delete_patient1'))
    elif action == 'view_by_id':
        return redirect(url_for('view_patient_by_id1'))
    elif action == 'view_by_name':
        return redirect(url_for('view_patients_by_name1'))
    elif action == 'view_by_disease':
        return redirect(url_for('view_patients_by_disease1'))
    elif action == 'view_all':
        return redirect(url_for('view_all_patients1'))
    else:
        return "Invalid action selected.", 400

@app.route('/patients/add')
def add_patient1():
    return render_template('add_patient.html')

@app.route('/patients/edit')
def edit_patient1():
    return render_template('edit_patient.html')

@app.route('/patients/delete')
def delete_patient1():
    return render_template('delete_patient.html')

@app.route('/patients/view_by_id')
def view_patient_by_id1():
    return render_template('view_patient_by_id.html')

@app.route('/patients/view_by_name')
def view_patients_by_name1():
    return render_template('view_patients_by_name.html')

@app.route('/patients/view_by_disease')
def view_patients_by_disease1():
    return render_template('view_patients_by_disease.html')

@app.route('/patients/view_all', methods = ['GET', 'POST'])
def view_all_patients1():
    patients = view_all_patients()
    if patients:
        return render_template('view_all_patients.html', patients = patients)
    else:
        flash(f"No Patients in Database Yet", "error")
        return redirect(url_for('patient_management'))
    return render_template('view_all_patients.html')

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient_to_db():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']
        medical_history = request.form['medicalHistory']
        id = add_patient(name, age, gender, disease, medical_history)
        print(id)
        flash(f"Patient added successfully patient ID: {id}!", "success")
        return redirect(url_for('add_patient1'))  
    return render_template('add_patient.html')

@app.route('/patients/edit', methods=['GET', 'POST'])
def edit_patient_from_db():
    if request.method == 'POST':
        id = request.form['patientID']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']
        medical_history = request.form['medicalHistory']
        if patient_exists(id):
            edit_patient(id, name, age, gender, disease, medical_history)
            flash(f"Edited Patients Details successfully!", "success")
            return redirect(url_for('edit_patient1'))  
        else:
            return redirect(url_for('edit_patient1'))  
    return render_template('edit_patient.html')

@app.route('/patients/delete', methods=['GET', 'POST'])
def delete_patient_from_db():
    if request.method == 'POST':
        id = request.form['patientID']
        if patient_exists(id):
            delete_patient(id)
            flash(f"Deleted Patient successfully!", "success")
            return redirect(url_for('delete_patient1')) 
        else:
            return redirect(url_for('delete_patient1'))
    return render_template('delete_patient.html')

@app.route('/patients/search_by_id', methods = ['GET', 'POST'])
def search_patient_by_id_from_db():
    if request.method == 'POST':
        id = request.form['patientID']
        patient = search_patient_by_id(id)
        if patient:
            return render_template('view_patient_by_id.html', patient = patient)
        else:
            flash(f"Patient with ID {id} does not exist.", "error")
            return redirect(url_for('view_patient_by_id1'))
    return render_template('view_patient_by_id.html')

@app.route('/patients/search_by_name', methods = ['GET', 'POST'])
def search_patients_by_name_from_db():
    if request.method == 'POST':
        name = request.form['name']
        patients = search_patients_by_name(name)
        if patients:
            return render_template('view_patients_by_name.html', patients = patients)
        else:
            flash(f"Patient with name: {name} does not exist.", "error")
            return redirect(url_for('view_patients_by_name1'))
    return render_template('view_patients_by_name.html')

@app.route('/patients/search_by_disease', methods = ['GET', 'POST'])
def search_patients_by_disease_from_db():
    if request.method == 'POST':
        disease = request.form['disease']
        patients = search_patients_by_disease(disease)
        if patients:
            return render_template('view_patients_by_disease.html', patients = patients)
        else:
            flash(f"Patient with disease: {disease} does not exist.", "error")
            return redirect(url_for('view_patients_by_disease1'))
    return render_template('view_patients_by_disease.html')

@app.route("/doctor")
def doctor_management():
    return render_template("doctor_management.html")

@app.route("/doctor/action", methods=["GET"])
def doctor_action():
    action = request.args.get("action")
    if action == 'add':
        return redirect(url_for('add_doctor1'))
    elif action == 'edit':
        return redirect(url_for('edit_doctor1'))
    elif action == 'delete':
        return redirect(url_for('delete_doctor1'))
    elif action == 'view_by_id':
        return redirect(url_for('view_doctor_by_id1'))
    elif action == 'view_by_name':
        return redirect(url_for('view_doctors_by_name1'))
    elif action == 'view_by_specialization':
        return redirect(url_for('view_doctors_by_specialization1'))
    elif action == 'view_by_current_status':
        return redirect(url_for('view_doctors_by_current_status1'))
    elif action == 'view_all':
        return redirect(url_for('view_all_doctors1'))
    else:
        return "Invalid action selected.", 400

@app.route('/doctors/add')
def add_doctor1():
    return render_template('add_doctor.html')

@app.route('/doctors/edit')
def edit_doctor1():
    return render_template('edit_doctor.html')

@app.route('/doctors/delete')
def delete_doctor1():
    return render_template('delete_doctor.html')

@app.route('/doctors/view_by_id')
def view_doctor_by_id1():
    return render_template('view_doctor_by_id.html')

@app.route('/doctors/view_by_name')
def view_doctors_by_name1():
    return render_template('view_doctors_by_name.html')

@app.route('/doctors/view_by_specialization')
def view_doctors_by_specialization1():
    return render_template('view_doctors_by_specialization.html')

@app.route('/doctors/view_by_current_status')
def view_doctors_by_current_status1():
    return render_template('view_doctors_by_current_status.html')

@app.route('/doctors/view_all', methods=['GET', 'POST'])
def view_all_doctors1():
    doctors = view_all_doctors()
    if doctors:
        return render_template('view_all_doctors.html', doctors = doctors)
    else:
        flash(f"No Doctors in Database Yet", "error")
        return redirect(url_for('doctor_management'))

@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor_to_db():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        specialization = request.form['specialization']
        current_status = request.form['status']
        id = add_doctor(name, age, gender, specialization, current_status)
        flash(f"Doctor added successfully Doctor ID: {id}!", "success")
        return redirect(url_for('add_doctor1'))  
    return render_template('add_doctor.html')

@app.route('/doctors/edit', methods=['GET', 'POST'])
def edit_doctor_from_db():
    if request.method == 'POST':
        id = request.form['doctorID']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        specialization = request.form['specialization']
        current_status = request.form['status']
        if doctor_exists(id):
            edit_doctor(id, name, age, gender, specialization, current_status)
            flash(f"Edited Doctor's Details successfully!", "success")
            return redirect(url_for('edit_doctor1'))  
        else:
            return redirect(url_for('edit_doctor1'))  
    return render_template('edit_doctor.html')

@app.route('/doctors/delete', methods=['GET', 'POST'])
def delete_doctor_from_db():
    if request.method == 'POST':
        id = request.form['doctorID']
        if doctor_exists(id):
            delete_doctor(id)
            flash(f"Deleted Doctor successfully!", "success")
            return redirect(url_for('delete_doctor1')) 
        else:
            return redirect(url_for('delete_doctor1'))
    return render_template('delete_doctor.html')

@app.route('/doctors/search_by_id', methods = ['GET', 'POST'])
def search_doctor_by_id_from_db():
    if request.method == 'POST':
        id = request.form['doctorID']
        doctor = search_doctor_by_id(id)
        if doctor:
            return render_template('view_doctor_by_id.html', doctor = doctor)
        else:
            flash(f"Doctor with ID {id} does not exist.", "error")
            return redirect(url_for('view_doctor_by_id1'))
    return render_template('view_doctor_by_id.html')

@app.route('/doctors/search_by_name', methods = ['GET', 'POST'])
def search_doctors_by_name_from_db():
    if request.method == 'POST':
        name = request.form['name']
        doctors = search_doctors_by_name(name)
        if doctors:
            return render_template('view_doctors_by_name.html', doctors = doctors)
        else:
            flash(f"Doctor with name: {name} does not exist.", "error")
            return redirect(url_for('view_doctors_by_name1'))
    return render_template('view_doctors_by_name.html')

@app.route('/doctors/search_by_specialization', methods = ['GET', 'POST'])
def search_doctors_by_specialization_from_db():
    if request.method == 'POST':
        specialization = request.form['specialization']
        doctors = search_doctors_by_specialization(specialization)
        if doctors:
            return render_template('view_doctors_by_specialization.html', doctors = doctors)
        else:
            flash(f"Doctor with Specialization: {specialization} does not exist.", "error")
            return redirect(url_for('view_doctors_by_specialization1'))
    return render_template('view_doctors_by_specialization.html')

@app.route('/doctors/search_by_status', methods = ['GET', 'POST'])
def search_doctors_by_status_from_db():
    if request.method == 'POST':
        status = request.form['status']
        doctors = search_doctors_by_current_status(status)
        if doctors:
            return render_template('view_doctors_by_current_status.html', doctors = doctors)
        else:
            flash(f"Doctor with Current Status: {status} does not exist.", "error")
            return redirect(url_for('view_doctors_by_current_status1'))
    return render_template('view_doctors_by_current_status.html')

@app.route("/appointment")
def appointment_management():
    return render_template("appointment_management.html")

@app.route("/appointment/action", methods=["GET"])
def appointment_action():
    action = request.args.get("action")

    if action == 'book':
        return redirect(url_for('book_appointment1'))
    elif action == 'reschedule':
        return redirect(url_for('reschedule_appointment1'))
    elif action == 'cancel':
        return redirect(url_for('cancel_appointment1'))
    elif action == 'view_by_id':
        return redirect(url_for('search_appointment_by_id1'))
    elif action == 'view_by_patient':
        return redirect(url_for('search_appointments_by_patient1'))
    elif action == 'view_by_doctor':
        return redirect(url_for('search_appointments_by_doctor1'))
    elif action == 'view_by_date':
        return redirect(url_for('search_appointments_by_date1'))
    elif action == 'view_all':
        return redirect(url_for('view_all_appointments1'))
    else:
        return "Invalid action selected.", 400
    
@app.route('/appointment/book')
def book_appointment1():
    return render_template('book_appointment.html')

@app.route('/appointment/reschedule')
def reschedule_appointment1():
    return render_template('reschedule_appointment.html')

@app.route('/appointment/cancel')
def cancel_appointment1():
    return render_template('cancel_appointment.html')

@app.route('/appointment/search_by_id')
def search_appointment_by_id1():
    return render_template('view_appointment_by_id.html')

@app.route('/appointment/search_by_patient')
def search_appointments_by_patient1():
    return render_template('view_appointments_by_patient.html')

@app.route('/appointment/search_by_doctor')
def search_appointments_by_doctor1():
    return render_template('view_appointments_by_doctor.html')

@app.route('/appointment/search_by_date')
def search_appointments_by_date1():
    return render_template('view_appointments_by_date.html')

@app.route('/appointment/view_all', methods=['GET', 'POST'])
def view_all_appointments1():
    appointments = view_all_appointments()
    if appointments:
        return render_template('view_all_appointments.html', appointments = appointments)
    else:
        flash(f"No Appointments Booked Yet", "error")
        return redirect(url_for('appointment_management'))

@app.route('/appointment/book', methods = ['GET', 'POST'])
def book_appointment_to_db():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        room_no = request.form['room_no']
        date_and_time = request.form['date_and_time']
        if patient_exists(patient_id):
            if doctor_exists(doctor_id):
                id = book_appointment(patient_id, doctor_id, room_no, date_and_time)
                flash(f"Appointment booked successfully appointment id: {id}!", "success")
                return redirect(url_for('book_appointment1'))
            else:
                return redirect(url_for("book_appointment1"))
        else:
            return redirect(url_for("book_appointment1"))
    return render_template('book_appointment.html')

@app.route('/appointment/reschedule', methods=['GET', 'POST'])
def reschedule_appointment_to_db():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        doctor_id = request.form['doctor_id']
        room_no = request.form['room_no']
        new_date_and_time = request.form['new_date_and_time']
        if appointment_booked(appointment_id):
            if doctor_exists(doctor_id):
                reschedule_appointment(appointment_id, doctor_id, room_no, new_date_and_time)
                flash("Appointment rescheduled successfully!", "success")
                return redirect(url_for('reschedule_appointment1'))
            else:
                return redirect(url_for('reschedule_appointment1'))
        else:
            return redirect(url_for('reschedule_appointment1'))
    return render_template('reschedule_appointment.html')

@app.route('/appointment/cancel', methods=['GET', 'POST'])
def cancel_appointment_form_db():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        if appointment_booked(appointment_id):
            cancel_appointment(appointment_id)
            flash("Appointment canceled successfully!", "success")
            return redirect(url_for('cancel_appointment1'))
        else:
            return redirect(url_for('cancel_appointment1'))
    return render_template('cancel_appointment.html')

@app.route('/appointment/search_by_id', methods=['GET', 'POST'])
def search_appointment_by_id_from_db():
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        appointment = search_appointment_by_id(appointment_id)
        if appointment:
            return render_template('view_appointment_by_id.html', appointment = appointment)
        else:
            flash(f"Appointment with id {appointment_id} does not exist", "error")
            return redirect(url_for("search_appointment_by_id1"))
    return render_template('view_appointment_by_id.html')

@app.route('/appointment/search_by_patient', methods=['GET', 'POST'])
def search_appointments_by_patient_from_db():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        appointments = search_appointments_by_patientId(patient_id)
        if appointments:
            return render_template('view_appointments_by_patient.html', appointments = appointments)
        else:
            flash(f"Appointment with Patient id {patient_id} does not exist", "error")
            return redirect(url_for("search_appointments_by_patient1"))
    return render_template('view_appointments_by_patient.html')


@app.route('/appointment/search_by_doctor', methods=['GET', 'POST'])
def search_appointments_by_doctor_from_db():
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        appointments = search_appointments_by_doctorId(doctor_id)
        if appointments:
            return render_template('view_appointments_by_doctor.html', appointments = appointments)
        else:
            flash(f"No appointments found for Doctor ID {doctor_id}", "error")
            return redirect(url_for("search_appointments_by_doctor1"))
    return render_template('view_appointments_by_doctor.html')

@app.route('/appointment/search_by_date', methods=['GET', 'POST'])
def search_appointments_by_date_from_db():
    if request.method == 'POST':
        appointment_date = request.form['appointment_date']
        appointments = search_appointments_by_dateAndTime(appointment_date)
        if appointments:
            return render_template('view_appointments_by_date.html', appointments = appointments)
        else:
            flash(f"No appointments found for the date {appointment_date}", "error")
            return redirect(url_for("search_appointments_by_date1"))
    return render_template('view_appointments_by_date.html')

@app.route("/billing")
def billing_management():
    return render_template("billing_management.html")

@app.route("/billing/action", methods = ['GET', 'POST'])
def billing_action():
    action = request.args.get("action")

    if action == 'generate':
        return redirect(url_for('generate_invoice1'))
    elif action == 'edit':
        return redirect(url_for('edit_invoice1'))
    elif action == 'delete':
        return redirect(url_for('delete_invoice1'))
    elif action == 'apply_discount':
        return redirect(url_for('apply_discount1'))
    elif action == 'search_by_id':
        return redirect(url_for('search_invoice_by_id1'))
    elif action == 'search_by_patient':
        return redirect(url_for('search_invoices_by_patient1'))
    elif action == 'view_all':
        return redirect(url_for('view_all_invoices1'))
    else:
        return "Invalid action selected.", 400

@app.route('/billing/generate')
def generate_invoice1():
    return render_template('generate_invoice.html')

@app.route('/billing/edit')
def edit_invoice1():
    return render_template('edit_invoice.html')

@app.route('/billing/delete')
def delete_invoice1():
    return render_template('delete_invoice.html')

@app.route('/billing/apply_discount')
def apply_discount1():
    return render_template('apply_discount.html')

@app.route('/billing/search_by_id')
def search_invoice_by_id1():
    return render_template('view_invoice_by_id.html')

@app.route('/billing/search_by_patient')
def search_invoices_by_patient1():
    return render_template('view_invoices_by_patient.html')

@app.route('/billing/view_all', methods = ['GET', 'POST'])
def view_all_invoices1():
    invoices = view_all_invoices()
    if invoices:
        return render_template('view_all_invoices.html', invoices = invoices)
    else:
        flash("No invoices found.", "error")
        return redirect(url_for('view_all_invoices1'))

@app.route('/billing/generate', methods=['GET', 'POST'])
def generate_invoice_to_db():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doc_fee = int(request.form['doc_fee'])
        medicine = int(request.form['medicine'])
        room_fee = int(request.form['room_fee'])
        other_expenses = int(request.form['other_expenses'])
        discount = int(request.form['discount'])
        if patient_exists(patient_id):
            invoice_id = generate_invoice(patient_id, doc_fee, medicine, room_fee, other_expenses, discount)
            flash(f"Invoice generated successfully with Invoice ID: {invoice_id}!", "success")
            return redirect(url_for('generate_invoice1'))
        else:
            return redirect(url_for('generate_invoice1'))
    return render_template('generate_invoice.html')

@app.route('/billing/edit', methods=['GET', 'POST'])
def edit_invoice_to_db():
    if request.method == 'POST':
        invoice_id = request.form.get('invoice_id')
        doc_fee = request.form.get('doc_fee', type=int)
        medicine = request.form.get('medicine', type=int)
        room_fee = request.form.get('room_fee', type=int)
        other_expenses = request.form.get('other_expenses', type=int)
        
        if invoice_generated(invoice_id):
            edit_invoice(invoice_id, doc_fee, medicine, room_fee, other_expenses)
            flash(f"Invoice {invoice_id} updated successfully!", "success")
            return redirect(url_for('edit_invoice1'))
        else:
            return redirect(url_for('edit_invoice1'))
    return render_template('edit_invoice.html')

@app.route('/billing/delete', methods=['GET', 'POST'])
def delete_invoice_from_db():
    if request.method == 'POST':
        invoice_id = int(request.form['invoice_id'])
        if invoice_generated(invoice_id):
            delete_invoice(invoice_id)
            flash(f"Invoice ID {invoice_id} deleted successfully!", "success")
            return redirect(url_for('delete_invoice1'))
        else:
            return redirect(url_for('delete_invoice1'))
    return render_template('delete_invoice.html')

@app.route('/billing/apply_discount', methods=['GET', 'POST'])
def apply_discount_to_db():
    if request.method == 'POST':
        invoice_id = int(request.form['invoice_id'])
        discount = int(request.form['discount'])

        if invoice_generated(invoice_id):
            apply_discount(invoice_id, discount)
            flash(f"Successfully applied Discount to invoice no: {invoice_id}", "success")
            return redirect(url_for('apply_discount1'))
        else:
            return redirect(url_for('apply_discount1'))
    return render_template('apply_discount.html')


@app.route('/billing/search_by_id', methods=['GET', 'POST'])
def search_invoice_by_id_from_db():
    if request.method == 'POST':
        invoice_id = request.form['invoice_id']
        invoice = search_invoice_by_id(invoice_id)
        if invoice:
            return render_template('view_invoice_by_id.html', invoice = invoice)
        else:
            flash(f"Invoice with ID {invoice_id} not found.", "error")
            return redirect(url_for('search_invoice_by_id1'))

    return render_template('view_invoice_by_id.html')


@app.route('/billing/search_by_patient', methods=['GET', 'POST'])
def search_invoices_by_patient_from_db():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        invoices = search_invoices_by_patientId(patient_id)
        if invoices:
            return render_template('view_invoices_by_patient.html', invoices = invoices)
        else:
            flash(f"No invoices found for Patient ID {patient_id}.", "error")
            return redirect(url_for('search_invoices_by_patient1'))

    return render_template('view_invoices_by_patient.html')

@app.route("/report")
def report_management():
    return render_template("report_management.html")

@app.route("/report/action", methods=["GET"])
def report_action():
    action = request.args.get("action")

    if action == 'total_patients_treated_for_specific_timeframe':
        return redirect(url_for('total_patients_treated_for_specific_timeframe1'))
    elif action == 'revenue_for_specific_timeframe':
        return redirect(url_for('revenue_for_specific_timeframe1'))
    elif action == 'doctor_performance':
        return redirect(url_for('doctor_performance1'))
    elif action == 'full_report':
        return redirect(url_for('full_report1'))
    else:
        return "Invalid action selected.", 400

@app.route('/report/total_patients_treated_for_specific_timeframe')
def total_patients_treated_for_specific_timeframe1():
    return render_template('total_patients_treated_for_specific_timeframe.html')

@app.route('/report/revenue_for_specific_timeframe')
def revenue_for_specific_timeframe1():
    return render_template('revenue_for_specific_timeframe.html')

@app.route('/report/doctor_performance', methods = ['GET', 'POST'])
def doctor_performance1():
    doctor_perform = doctor_performance()
    if doctor_perform:
        return render_template('doctor_performance.html', doctor_perform = doctor_perform)
    else:
        flash("No Data Yet🥲", "error")
        return redirect(url_for("report_management"))

@app.route('/report/full_report')
def full_report1():
    total_patients, revenue, doctor_perform = full_report()
    if total_patients or revenue or doctor_perform:
        return render_template('full_report.html', total_patients = total_patients, revenue = revenue, doctor_perform = doctor_perform)
    else:
        flash("No Data Yet🥲", "error")
        return redirect(url_for("report_management"))

@app.route('/report/total_patients_treated_for_specific_timeframe', methods = ['GET', 'POST'])
def total_patients_treated_for_specific_timeframe_in_db():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        patients_treated = total_patients_treated_for_specific_timeframe(start_date, end_date)
        return render_template('total_patients_treated_for_specific_timeframe.html', patients_treated = patients_treated, start_date = start_date, end_date = end_date)
    
@app.route('/report/revenue_for_specific_timeframe', methods = ['GET', 'POST'])
def revenue_for_specific_timeframe_from_db():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        revenue_generated = revenue_for_specific_timeframe(start_date, end_date)
        return render_template('revenue_for_specific_timeframe.html', revenue_generated = revenue_generated, start_date = start_date, end_date = end_date)





if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Render gives you a PORT automatically
    app.run(host="0.0.0.0", port=port)