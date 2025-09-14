from Database import createTables, createDatabase
from flask import flash

connection = createDatabase()
createTables()
cursor = connection.cursor()

def generate_invoice(patient_id, doc_fee, medicine, room_fee, other_expences, discount):
    total_amount = doc_fee + medicine + room_fee + other_expences
    final_amount = total_amount - (total_amount * discount / 100)
    cursor.execute('''INSERT INTO bills (patient_id, doc_fee, medicine, room_fee, other_expences, total_amount, discount, final_amount)
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', (patient_id, doc_fee, medicine, room_fee, other_expences, total_amount, discount, final_amount))
    connection.commit()
    invoice_id = cursor.lastrowid
    return invoice_id

def edit_invoice(invoice_id, doc_fee = None, medicine = None, room_fee = None, other_expences = None):
    cursor.execute("SELECT discount FROM bills WHERE id = ?", (invoice_id,))
    discount = cursor.fetchone()[0]
    if doc_fee is None:
        cursor.execute("SELECT doc_fee FROM bills WHERE id = ?", (invoice_id,))
        doc_fee = cursor.fetchone()[0]

    if medicine is None:
        cursor.execute("SELECT medicine FROM bills WHERE id = ?", (invoice_id,))
        medicine = cursor.fetchone()[0]

    if room_fee is None:
        cursor.execute("SELECT room_fee FROM bills WHERE id = ?", (invoice_id,))
        room_fee = cursor.fetchone()[0]

    if other_expences is None:
        cursor.execute("SELECT other_expences FROM bills WHERE id = ?", (invoice_id,))
        other_expences = cursor.fetchone()[0]

    total_amount = doc_fee + medicine + room_fee + other_expences
    final_amount = total_amount - (total_amount * discount / 100)

    if doc_fee:
        cursor.execute("UPDATE bills SET doc_fee = ? WHERE id = ?", (doc_fee, invoice_id))
    if medicine:
        cursor.execute("UPDATE bills SET medicine = ? WHERE id = ?", (medicine, invoice_id))
    if room_fee:
        cursor.execute("UPDATE bills SET room_fee = ? WHERE id = ?", (room_fee, invoice_id))
    if other_expences:
        cursor.execute("UPDATE bills SET other_expences = ? WHERE id = ?", (other_expences, invoice_id))

    cursor.execute("UPDATE bills SET total_amount = ? WHERE id = ?", (total_amount, invoice_id))
    cursor.execute("UPDATE bills SET final_amount = ? WHERE id = ?", (final_amount, invoice_id))

    connection.commit()

def delete_invoice(invoice_id):
    cursor.execute("DELETE FROM bills WHERE id = ?", (invoice_id,))
    connection.commit()

def search_invoice_by_id(invoice_id):
    cursor.execute("SELECT * FROM bills WHERE id = ?", (invoice_id,))
    invoice = cursor.fetchone()
    return invoice

def search_invoices_by_patientId(patient_id):
    cursor.execute("SELECT * FROM bills WHERE patient_id = ?", (patient_id,))
    invoices = cursor.fetchall()
    return invoices

def apply_discount(invoice_id, discount):
    cursor.execute("SELECT total_amount FROM bills WHERE id = ?", (invoice_id,))
    total_amount = cursor.fetchone()[0]
    final_amount = total_amount - (total_amount * discount / 100)
    cursor.execute("UPDATE bills SET discount = ?, final_amount = ? WHERE id = ?", (discount, final_amount, invoice_id))
    connection.commit()

def view_all_invoices():
    cursor.execute("SELECT * FROM bills")
    invoices = cursor.fetchall()
    return invoices

def invoice_generated(invoice_id):
    cursor.execute("SELECT 1 FROM bills WHERE id = ?", (invoice_id,))
    if cursor.fetchone() is None:
        flash(f"Invoice with ID {invoice_id} does not exist.", "error")
        return False
    return True