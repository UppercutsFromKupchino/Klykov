import psycopg2
import psycopg2.extras
import psycopg2.errors
from flask import session


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_user(self, email):
        self.__cursor.execute(f"SELECT * FROM patient WHERE email = '{email}' ")
        user = self.__cursor.fetchone()
        if not user:
            return False
        return user

    def add_user(self, email, password, fio, sex, age):
        self.__cursor.execute(f"INSERT INTO patient VALUES {email, password, fio, sex, age}")
        self.__db.commit()
        
    def get_doctor_schedule(self, doctor):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute(f"SELECT weekday FROM schedule WHERE doc_fio = '{doctor}' ")
        doctor_sched = self.__cursor.fetchall()
        return doctor_sched
    
    def get_spec(self):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute(f"SELECT name FROM specialization")
        spec = self.__cursor.fetchall()
        return spec
    
    def get_doctor(self):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute(f"SELECT fio FROM doctor")
        doctor = self.__cursor.fetchall()
        return doctor
    
    def get_doctor_from_spec(self, spec):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute(f"SELECT fio FROM doctor WHERE spec = '{spec}'")
        doctor = self.__cursor.fetchall()
        return doctor
        
    def get_patient_coup(self, email):
        self.__cursor = self.__db.cursor()
        self.__cursor.execute(f"SELECT doc_fio FROM coupon WHERE pat_email = '{email}' ")
        doctors = self.__cursor.fetchall()
        return doctors

    def add_coupon(self, email, doctor, day, time, off_num):
        self.__cursor.execute(f"INSERT INTO coupon VALUES {day, time, doctor, off_num, email}")
        self.__db.commit()

    def get_tt_of_doctor(self, day, fio):
        self.__cursor.execute(f"""SELECT time, doc_fio FROM schedule WHERE weekday = '{day}' AND doc_fio = '{fio}'""")
        result = self.__cursor.fetchall()
        return result

    def add_coupon_patient(self, patient, date, time, doc_fio):
        self.__cursor.execute(f"""INSERT INTO coupon(date,time,doc_fio,pat_email) VALUES('{date}','{time}','{doc_fio}',
                              '{patient}')""")
        self.__db.commit()

    def update_age(self, age, email):
        self.__cursor.execute(f"""UPDATE patient SET age='{age}'""")
        self.__db.commit()

    def get_coupons_patient(self, patient):
        self.__cursor.execute(f"""SELECT date, time, doc_fio FROM coupon WHERE pat_email ='{patient}'""")
        result = self.__cursor.fetchall()
        return result
        
    