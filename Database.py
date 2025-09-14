import sqlite3

def createDatabase():
    connection = sqlite3.connect("HMS_Database.db", check_same_thread= False)
    return connection

def createTables():
    connection = createDatabase()
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER,
                        gender TEXT CHECK(gender IN ('M', 'F')) NOT NULL,
                        disease TEXT,
                        medical_history TEXT,
                        admit_date TEXT DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER,
                        gender TEXT CHECK(gender IN ('M', 'F')) NOT NULL,
                        specialization TEXT,
                        current_status TEXT CHECK(current_status IN ('Free', 'Reserved')) NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER,
                        doctor_id INTEGER,
                        room_no INTEGER,
                        dateAndTime TEXT,
                        FOREIGN KEY(patient_id) REFERENCES patients(id),
                        FOREIGN KEY(doctor_id) REFERENCES doctors(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS bills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER,
                        doc_fee REAL,
                        medicine REAL,
                        room_fee REAL,
                        other_expences REAL,
                        total_amount REAL,
                        discount REAL DEFAULT 0,
                        final_amount REAL,
                        billing_date TEXT DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(patient_id) REFERENCES patients(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS room (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room_no INTEGER,
                        patient_id INTEGER,
                        admission_date TEXT,
                        discharge_date TEXT,
                        FOREIGN KEY(patient_id) REFERENCES patients(id))''')

    connection.commit()
    connection.close()


