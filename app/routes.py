from app import app
from flask import render_template, redirect, request, url_for, g, flash, session
import psycopg2
import psycopg2.extras
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.userlogin import UserLogin
from app.database import DataBase
from app.forms import LoginForm, RegisterForm, ChooseTimetableDoctor, ExecuteTimetable, UpdateAge

# инициализация менеджера логинов
login_manager = LoginManager(app)


# Login-manager
@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id, dbase)


# Подключение к СУБД через драйвер psycopg2
def connect_db():
    conn = psycopg2.connect(dbname="da8agpdf6ikrco",
                            user="yivdfsgbnztgnx",
                            password="ad4b108a76fa1f52710a8568a9b2ff961548edba0f5e6c96477872dfb6803af2",
                            host="ec2-54-78-36-245.eu-west-1.compute.amazonaws.com")
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# Создание объекта для работы с бд
@app.before_request
def before_request():
    db = get_db()
    global dbase
    dbase = DataBase(db)


# Закрытие работы с базой данных
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# Декораторы маршрутов
@app.route('/')
def index():
    if current_user.is_authenticated:
        login_user = session['email']
        return render_template('index.html', login_user=login_user)
    return render_template('index.html')


@app.route('/autorization', methods=['GET', 'POST'])
def autorization():
    login_form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Проверка валидации формы, введённой на сайте
    if login_form.validate_on_submit():
        # Проверяю, существует ли в базе данных пользователь с логином, введённым в форме
        user = dbase.get_user(login_form.email_loginform.data)
        if user:
            # Авторизация пользователя
            user_login = UserLogin().create(user)
            login_user(user_login)
            session['email'] = user['email']

            return redirect(url_for('index'))

    return render_template('autorization.html', login_form=login_form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        user = dbase.get_user(reg_form.email_regform.data)
        if user:
            flash("Аккаунт уже существует")
            redirect(url_for('registration'))
        else:
            dbase.add_user(reg_form.email_regform.data, reg_form.password_regform.data, reg_form.fio_regform.data, reg_form.sex_regform.data, reg_form.age_regform.data)

            return redirect(url_for('index'))
        
    return render_template('registration.html', reg_form=reg_form)


@app.route('/patientprofile', methods=['GET', 'POST'])
def patientprofile():
    update_age = UpdateAge()
    pat_prof = dbase.get_user(session['email'])
    pat_email = pat_prof[0]
    pat_fio = pat_prof[2]
    pat_age = pat_prof[4]

    if update_age.submit.data:

        dbase.update_age(update_age.age.data, current_user.get_id())
        return redirect(url_for('patientprofile'))

    return render_template('patient_profile.html', pat_email=pat_email, pat_fio=pat_fio,pat_age=pat_age,
                           update_age=update_age)


@app.route('/patientcoupons', methods=['GET', 'POST'])
def patientcoupons():

    coupons = dbase.get_coupons_patient(current_user.get_id())
    coupons_len = len(coupons)

    return render_template("patient_coupons.html", coupons=coupons, coupons_len=coupons_len)


@app.route('/doctorcoupons', methods=['GET', 'POST'])
def doctorcoupons():
    return render_template('doctor_coupons.html')


@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():

    choose_timetable_doctor = ChooseTimetableDoctor()
    doctors = dbase.get_doctor()
    choose_timetable_doctor.doctor.choices = [i[0] for i in doctors]

    if choose_timetable_doctor.submit_choose.data:
        date = choose_timetable_doctor.date.data
        doctor = choose_timetable_doctor.doctor.data
        return redirect(url_for('add_coupon', date=date, doctor=doctor))

    return render_template('appointment.html', choose_timetable_doctor=choose_timetable_doctor)


@app.route('/add_coupon/<date>/<doctor>', methods=['GET', 'POST'])
def add_coupon(date, doctor):
    doctor = doctor
    date = date

    timetable = dbase.get_tt_of_doctor(date, doctor)
    timetable_len = len(timetable)

    execute_timetable = ExecuteTimetable()

    if execute_timetable.submit_execute.data:
        print("zbs")

        dbase.add_coupon_patient(current_user.get_id(), date, execute_timetable.time.data, doctor)

    return render_template("add_coupon.html", timetable=timetable, timetable_len=timetable_len,
                           execute_timetable=execute_timetable, doctor=doctor, date=date)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('index'))
