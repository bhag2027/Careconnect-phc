from flask import *
from database import *
import uuid
import os
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

public=Blueprint('public',__name__)

# @public.route('/')
# def homepage():
# 	return render_template('homepage.html')  

from datetime import datetime

@public.route('/')
def homepage():
    data = {}
    q = "SELECT * FROM event ORDER BY event_id DESC"
    event_data = select(q)

    # Convert time format to 12-hour with AM/PM
    for row in event_data:
        try:
            row['time'] = datetime.strptime(row['time'], "%H:%M:%S").strftime("%I:%M %p")
        except:
            row['time'] = row['time']  # Fallback if format is already correct or missing

    data['view'] = event_data

    return render_template('homepage.html', data=data)



@public.route('/login',methods=['get','post'])
def login():

	if 'submit' in request.form:
		uname=request.form['uname']
		passs=request.form['pwd']
		q="SELECT * FROM `login` WHERE username='%s' "%(uname)
		res=select(q)
		if res:
			stored_hash = res[0]['password']
			session['lid']=res[0]['login_id']
   
			if res[0]['user_type']=='admin':
				flash('WELCOME TO ADMIN HOME')
				return redirect(url_for('admin.adminhome'))

			if res[0]['user_type']=='hospital':
				print("jjjjjjjjjjjjjjjjjjj")
				# if check_password_hash(stored_hash, passs):
				q="SELECT * FROM hospitals WHERE `login_id`='%s'"%(res[0]['login_id'])
				res2=select(q)
				session['hid']=res2[0]['hospital_id']
				session
				flash('WELCOME TO HOSPITAL HOME')
				return redirect(url_for('hospital.hospitalhome'))
					
			if res[0]['user_type']=='doctor':
				if check_password_hash(stored_hash, passs):
					q="SELECT * FROM doctor WHERE `login_id`='%s'"%(res[0]['login_id'])
					res2=select(q)
					session['did']=res2[0]['doctor_id']
					flash('WELCOME TO DOCTOR HOME')
					return	redirect(url_for('doctor.doctor_home'))

			if res[0]['user_type']=='pharmacy':
				if check_password_hash(stored_hash, passs):
					q="SELECT * FROM pharmacy WHERE `login_id`='%s'"%(res[0]['login_id'])
					rr=select(q)
					session['phid']=rr[0]['pharmacy_id']
					flash('WELCOME TO PHARMACY HOME')
					return	redirect(url_for('pharmacy.pharmacyhome'))



			if res[0]['user_type']=='patient':
				if check_password_hash(stored_hash, passs):
					q="SELECT * FROM patients WHERE `login_id`='%s'"%(res[0]['login_id'])
					rr=select(q)
					session['pid']=rr[0]['patient_id']
					flash('WELCOME TO PATIENT HOME')
					return	redirect(url_for('user.user_home'))

			if res[0]['user_type']=='aasha_worker':
				if check_password_hash(stored_hash, passs):
					q="SELECT * FROM aasha_worker WHERE `login_id`='%s'"%(res[0]['login_id'])
					rr=select(q)
					session['aasha_worker']=rr[0]['aasha_worker_id']
					flash('WELCOME TO JHI HOME')
					return	redirect(url_for('aasha_worker.aasha_worker_home'))

			if res[0]['user_type']=='lab':
				if check_password_hash(stored_hash, passs):
					q="SELECT * FROM lab WHERE `login_id`='%s'"%(res[0]['login_id'])
					rr=select(q)
					session['lab']=rr[0]['lab_id']
					flash('WELCOME TO LABORATORY HOME')
					return	redirect(url_for('lab.lab_home'))

		else:
			flash("Username Or password Is Wrong")
	return render_template('login.html')

@public.route('/registration',methods=['get','post'])
def registration():

	if 'submit' in request.form:
		uname=request.form['Username']
		pword=request.form['password']
		hashed_pwd = generate_password_hash(pword)
		hname=request.form['Hospitalname']
		place=request.form['Place']
		landmark=request.form['landmark']
		latitiude=request.form['latitude']
		longitude=request.form['longitude']
		phone=request.form['phone']
		email=request.form['email']
		photo=request.files['photo']
  
		upload_folder = "static/images/"
		if not os.path.exists(upload_folder):
			os.makedirs(upload_folder)
		path = os.path.join(upload_folder, str(uuid.uuid4()) + photo.filename)
		photo.save(path)

		q="INSERT INTO `login`(`username`,`password`,`user_type`)VALUES('%s','%s','pending')"%(uname,hashed_pwd)
		id=insert(q)
		q1="INSERT INTO  hospitals VALUES(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','pending')"%(id,hname,place,landmark,latitiude,longitude,phone,email,path)
		insert(q1)
		flash("REGISTERED")
		return redirect(url_for('public.login'))
	return render_template('registration.html')
@public.route('/patient_registration', methods=['GET', 'POST'])
def patient_registration():
    if 'submit' in request.form:
        uname = request.form['un']
        pword = request.form['pw']
        hashed_pwd = generate_password_hash(pword)
        fn = request.form['fn']
        ln = request.form['ln']
        place = request.form['Place']
        dob = request.form['dob']
        gen = request.form['gen']
        phone = request.form['phone']
        email = request.form['email']

        # Check if username already exists
        q_check_uname = "SELECT * FROM login WHERE username='%s'" % (uname)
        res_uname = select(q_check_uname)

        # Check if email already exists
        q_check_email = "SELECT * FROM patients WHERE email='%s'" % (email)
        res_email = select(q_check_email)

        if res_uname:
            flash("Username already exists! Please choose a different one.", "danger")
        elif res_email:
            flash("Email is already registered! Try logging in.", "danger")
        else:
            # Insert into login table
            q = "INSERT INTO `login`(`username`,`password`,`user_type`) VALUES('%s','%s','patient')" % (uname, hashed_pwd)
            id = insert(q)

            # Insert into patients table
            q1 = "INSERT INTO patients VALUES(null,'%s','%s','%s','%s','%s','%s','%s','%s')" % (id, fn, ln, dob, gen, place, phone, email)
            insert(q1)

            flash("Registration Successful! You can now log in.", "success")
            return redirect(url_for('public.login'))

    return render_template('patient_registration.html')


@public.route('/pharmacy_registration',methods=['get','post'])
def pharmacy_registration():

	if 'submit' in request.form:
		uname=request.form['Username']
		pword=request.form['password']
		hashed_pwd = generate_password_hash(pword)
		hname=request.form['pname']
		place=request.form['Place']
		landmark=request.form['landmark']
		phone=request.form['phone']
		email=request.form['email']

		q="INSERT INTO `login`(`username`,`password`,`user_type`)VALUES('%s','%s','pharmacy')"%(uname,hashed_pwd)
		id=insert(q)
		t="insert into pharmacy values(null,'%s','%s','%s','%s','%s','%s')"%(id,hname,place,landmark,phone,email)
		insert(t)
		flash("REGISTERED..........")
		return redirect(url_for('public.login'))
	return render_template('pharmacy_reg.html')

@public.route('/aasha_worker_registration',methods=['get','post'])
def aasha_worker_registration():
	if 'submit' in request.form:
		uname=request.form['un']
		pword=request.form['pw']
		hashed_pwd = generate_password_hash(pword)
		fn=request.form['fn']
		ln=request.form['ln']
		city=request.form['city']
		phone=request.form['phone']
		email=request.form['email']

		q="INSERT INTO `login`(`username`,`password`,`user_type`)VALUES('%s','%s','aasha_worker')"%(uname,hashed_pwd)
		id=insert(q)
		q1="INSERT INTO  aasha_worker VALUES(null,'%s','%s','%s','%s','%s','%s')"%(id,fn,ln,city,phone,email)
		insert(q1)
		flash("REGISTERED")
		return redirect(url_for('public.login'))
	return render_template('aasha_worker_registration.html')  

from datetime import datetime

@public.route('/publick_view_event')
def publick_view_event():
    data = {}
    vv = "SELECT * FROM event ORDER BY event_id DESC"  # Fetch newest events first
    event_data = select(vv)  

    # Convert time to 12-hour format with AM/PM
    for row in event_data:
        row['time'] = datetime.strptime(row['time'], "%H:%M:%S").strftime("%I:%M %p")

    data['view'] = event_data

    return render_template('publick_view_event.html', data=data)

