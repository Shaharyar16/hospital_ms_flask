from Database import createTables, createDatabase

connection = createDatabase()
createTables()
cursor = connection.cursor()

def total_patients_treated_for_specific_timeframe(start_date, end_date):
    cursor.execute("SELECT COUNT(*) FROM patients WHERE admit_date BETWEEN ? AND ?", (start_date, end_date))
    total_patients = cursor.fetchone()[0]
    return total_patients
    connection.commit()

def revenue_for_specific_timeframe(start_date, end_date):
    cursor.execute("SELECT SUM(final_amount) from bills WHERE billing_date BETWEEN ? AND ?", (start_date, end_date))
    revenue = cursor.fetchone()[0]
    return revenue
    connection.commit()

def doctor_performance():
        cursor.execute("SELECT doctor_id, COUNT(patient_id) FROM appointments GROUP BY doctor_id ORDER BY COUNT(patient_id) DESC")
        result = cursor.fetchall()
        return result
        connection.commit()

def full_report():
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(final_amount) from bills")
    revenue = cursor.fetchone()[0]

    cursor.execute("SELECT doctor_id, COUNT(patient_id) FROM appointments GROUP BY doctor_id ORDER BY COUNT(patient_id) DESC")
    result = cursor.fetchall()

    return total_patients, revenue, result