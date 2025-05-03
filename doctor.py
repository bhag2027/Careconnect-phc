from flask import *
from database import *
import uuid



import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail



doctor=Blueprint('doctor',__name__)

@doctor.route('/doctor_home')
def doctor_home():
	return render_template('doctor_home.html')  

@doctor.route('/doctor_viewappointment')
def doctor_viewappointment():
    data = {}
    did = session['did']  # Doctor ID from session

    # Get search date from request
    search_date = request.args.get('search_date')

    # Base query
    q = """SELECT *, CONCAT(patients.first_name, ' ', patients.last_name) AS patient_name,
                  CONCAT(doctor.first_name, ' ', doctor.last_name) AS doctor_name
           FROM appointments
           INNER JOIN doctor USING (doctor_id)
           INNER JOIN patients USING (patient_id)
           WHERE doctor_id = '%s'""" % did  # Fetch only this doctor's appointments

    if search_date:
        q += " AND appointment_date = '%s'" % search_date  # Add date filter

    res = select(q)  # Fetch data
    data['appointment'] = res

    # Check if there are no appointments and set a flag
    data['no_appointments'] = len(res) == 0

    action = request.args.get('action')
    appointment_id = request.args.get('appointment_id')

    if action == 'test_request':
        check_query = "SELECT * FROM test_reult WHERE appointment_id = '%s'" % appointment_id
        ff = select(check_query)
        if ff:
            flash("Request already sent ...")
        else:
            insert_query = "INSERT INTO test_reult VALUES (NULL, '%s', 'pending', 'pending', 'pending', 'pending', 'pending')" % appointment_id
            insert(insert_query)
            flash("Request sent successfully...")

        return redirect(url_for('doctor.doctor_viewappointment', search_date=search_date))

    if action == 'appoint':
        update_query = "UPDATE appointments SET status='appointed' WHERE appointment_id = '%s'" % appointment_id
        update(update_query)
        return redirect(url_for('doctor.doctor_viewappointment', search_date=search_date))

    if action == 'cancel':
        update_query = "UPDATE appointments SET status='cancelled' WHERE appointment_id = '%s'" % appointment_id
        update(update_query)
        return redirect(url_for('doctor.doctor_viewappointment', search_date=search_date))

    return render_template('doctor_viewappointment.html', data=data, search_date=search_date)




@doctor.route('/doctor_fee',methods=['post','get'])
def doctor_fee():
	if 'submit' in request.form:
		fee=request.form['fee']
		aid=request.args['aid']
		q="update appointments set amount='%s' where appointment_id='%s'"%(fee,aid)
		update(q)
		flash("paid successfully...")
	return render_template('doctor_fee.html')


@doctor.route('/doctorviewfiles')
def doctorviewfiles():

	data={}
	pid=request.args['pid']
	data['pid']=pid

	if 'action' in request.args:
		action=request.args['action']
		mid=request.args['mid']
	else:
		action=None
	if action=="request":
		q="insert into requests values(null,'%s','%s',curdate(),'pending')" %(mid,session['did'])
		insert(q)
		return redirect(url_for('doctor.doctorviewfiles',pid=pid))
		
	q="select * from medical_records where patient_id='%s'" %(pid)
	res=select(q);
	data['files']=res


	return render_template('doctorviewfiles.html',data=data)

@doctor.route('/doctorviewequestedfiles', methods=['get','post'])
def  doctorviewequestedfiles():
	data={}
	pid=request.args['pid']
	did=session['did']
	q="SELECT * FROM  medical_records inner join requests USING(medical_record_id) where patient_id='%s' and requests.doctor_id='%s'" %(pid,did)
	print(q)
	res=select(q)
	print(res)
	data['val']=res
	
  
	if 'mid' in request.args:
		data['mid']=request.args['mid']
		print(data['mid'])
		return redirect(url_for('doctor.download',mid=request.args['mid']))


	return render_template("doctorviewequestedfiles.html",data=data)

@doctor.route('/doctor_managedisease',methods=['get','post'])
def doctor_managedisease():
	data={}
	q="select * from diseases where doctor_id='%s'" %(session['did'])
	res=select(q)
	data['diseases']=res
	if 'submit' in request.form:
		title=request.form['title']
		description=request.form['descri']
		symptoms=request.form['sym']
		date_time=request.form['dt']

		q="INSERT INTO `diseases`(`doctor_id`,`title`,`description`,`symptoms`,`date_time`)VALUES('%s','%s','%s','%s','%s')"%(session['did'],title,description,symptoms,date_time)
		insert(q)
		
		return redirect(url_for('doctor.doctor_managedisease'))

	return render_template('doctor_managedisease.html',data=data)


@doctor.route('/doctor_uploadmedicalreports', methods=['get', 'post'])
def doctor_uploadmedicalreports():
    data = {}
    pid = request.args['pid']
    did = session['did']
    data['name'] = request.args['name']

    q = "select * from medical_records where doctor_id='%s' and patient_id='%s' and uploaded_by='doctor'" % (pid, did)
    res = select(q)
    data['upload'] = res

    if 'submit' in request.form:
        file = request.files['file']
        
        # Validate file extension
        if not file.filename.lower().endswith('.pdf'):
            flash("❌ Only PDF files are allowed.")
            return redirect(url_for('doctor.doctor_uploadmedicalreports', pid=pid, name=data['name']))

        # Save the PDF file
        path = "static/uploads/" + str(uuid.uuid4()) + file.filename
        file.save(path)

        q = "INSERT INTO medical_records(patient_id, doctor_id, uploaded_by, file, date_time) VALUES('%s','%s','doctor','%s',NOW())" % (pid, did, path)
        insert(q)
        flash("✅ PDF uploaded successfully.")
        return redirect(url_for('doctor.doctor_uploadmedicalreports', pid=pid, name=data['name']))

    return render_template('doctor_uploadmedicalreports.html', data=data)

# @doctor.route('/doctorviewpatients')
# def doctorviewpatients():

# 	data={}

# 	q="SELECT *,CONCAT(`first_name`,' ',`last_name`) AS patient_name FROM `appointments` INNER JOIN `patients` USING(patient_id) "
# 	res=select(q)
# 	data['appointment']=res
# 	return render_template("doctorviewpatients.html",data=data)

@doctor.route('/doctor_view_user')
def doctor_view_user():
    data = {}
    did = session.get('did')  # Get doctor ID safely

    if not did:
        flash("Session expired. Please log in again.")
        return redirect(url_for('login'))  # Redirect if session is missing

    # Get search date from request
    search_date = request.args.get('search_date')

    # Fetch only "Remote Consultation" patients
    q = """
        SELECT DISTINCT patients.first_name, patients.last_name, patients.phone,patients.dob,patients.place,
                        patients.login_id, appointments.appointment_date, appointments.time 
        FROM appointments 
        INNER JOIN patients USING(patient_id)
        WHERE appointments.doctor_id = %s
        AND appointments.type = 'Remote Consultation'
    """ % did

    if search_date:
        q += " AND appointments.appointment_date = '%s'" % search_date  # Filter by date

    res = select(q)  # Execute query
    data['appointments'] = res

    # Check if there are no appointments and set a flag
    data['no_appointments'] = len(res) == 0

    return render_template('doctorviewallpatients.html', data=data, search_date=search_date)





	
@doctor.route('/doctorviewuploadedfiles', methods=['get','post'])
def  doctorviewuploadedfiles():
	data={}
	pid=request.args['pid']
	data['pid']=pid
	print(pid)
	did=session['did']
	if "submit" in request.form:
		key=request.form['key']
		q="select * from medical_reports where mid='%s' and key='%s'" %(request.args['mid'],key)
		res=select(q)
		if res:
			return redirect(url_for('doctor.download',mid=request.args['mid']))
    # key="haiiiiii"
    # log=session['logid']
	if 'mid' in request.args:
		data['mid']=request.args['mid']

	else:
		q="select *,concat(first_name,' ',last_name) as dname from shared inner join medical_records using(medical_record_id) inner join doctor on medical_records.doctor_id=doctor.doctor_id where patient_id='%s' and shared.doctor_id='%s'" %(pid,did)
		print(q)
		res=select(q)
		print(res)
		data['val']=res

	return render_template("doctorviewuploadedfiles.html",data=data)


# @doctor.route('/download')
# def download():
#     mid = request.args['mid']
#     q="select file from medical_records where medical_record_id='%s'"%(mid)
#     res=select(q)
#     path=res[0]['file']
#     print(path)
#     # data = download(mid)
#     print("path : "+path[::-1])

#     filename="static/downloads/"+str(uuid.uuid4())+path
#     print(filename)
   
#     file = open(path, "rb")
#     data = file.read()
#     # pritn(data)
#     return Response(data,
#                     mimetype="text/plain",
#                     headers={"Content-Disposition":
#                                  "attachment;filename=%s" % filename})

	




@doctor.route('/doctoruploadprescription', methods=['get','post'])
def doctoruploadprescription():
    data = {}
    aid = request.args['aid']

   
    q = """
    SELECT prescription.*, CONCAT(doctor.first_name, ' ', doctor.last_name) AS doctor_name
    FROM prescription
    INNER JOIN appointments USING(appointment_id)
    INNER JOIN doctor ON appointments.doctor_id = doctor.doctor_id
    WHERE prescription.appointment_id='%s'
    """ % (aid)
    
    res = select(q)
    if res:
        data['p'] = res

   
    if "submit" in request.form:
        p = request.form['p']
        q = "INSERT INTO prescription VALUES(NULL, '%s', '%s', NOW(), 'pending', 'pending')" % (aid, p)
        insert(q)
        flash("Added successfully")
        return redirect(url_for('doctor.doctoruploadprescription', aid=aid))

    
    if 'action' in request.args:
        action = request.args['action']
        pid = request.args['pid']
    else:
        action = None

    if action == 'delete':
        aid = request.args['aid']
        q = "DELETE FROM prescription WHERE prescription_id='%s'" % (pid)
        delete(q)
        flash("Deleted successfully")
        return redirect(url_for('doctor.doctoruploadprescription', aid=aid))

    
    if action == 'update':
        e = "SELECT * FROM prescription WHERE prescription_id='%s'" % (pid)
        data['up'] = select(e)

    if 'update' in request.form:
        p = request.form['p']
        q = "UPDATE prescription SET prescription='%s' WHERE prescription_id='%s'" % (p, pid)
        update(q)
        flash("Updated successfully")
        return redirect(url_for('doctor.doctoruploadprescription', aid=aid))

    return render_template("doctoruploadprescription.html", data=data)



@doctor.route('/doctor_chat',methods=['get','post'])
def doctor_chat():
	data={}
	print("$$$$$$$$$$$$$$$$$$$$$$$$$")
	ulid=request.args['id']
	did=session['did']
	data['did']=session['lid']
	name=request.args['name']
	data['name']=name
	print(ulid,did)
	q="select * from messages where (sender_id='%s' and receiver_id='%s') or (sender_id='%s' and receiver_id='%s') "%(ulid,session['lid'],session['lid'],ulid)
	print("cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",q)
	res=select(q)
	print(res)
	data['chat']=res
	if 'submit' in request.form:
		msg=request.form['msg']
		q="insert into messages value(NULL,'%s','patient','%s','doctor','%s',NOW())"%(session['lid'],ulid,msg)
		insert(q)
		return redirect(url_for('doctor.doctor_chat',name=name,id=ulid))
	return render_template('doctor_chat.html',data=data)


@doctor.route('/admin_view_disease_symptom',methods=['get','post'])
def admin_view_disease_symptom():
	data={}
	q="select * from diseases " 
	res=select(q)
	data['diseases']=res
	if 'submit' in request.form:
		title=request.form['title']
		description=request.form['descri']
		q="INSERT INTO diseases VALUES(null,'%s','%s')"%(title,description)
		insert(q)
		flash("Disease added successfully..")
		return redirect(url_for('doctor.admin_view_disease_symptom'))
		
	if 'action' in request.args:
			action=request.args['action']
			d_id=request.args['disease_id']

	else:
		action=None

	if action=='delete':
		q="delete from diseases where disease_id='%s'"%(d_id)
		delete(q)
	
		flash("Deleted........!")
		return redirect(url_for('doctor.admin_view_disease_symptom'))

	if action=='update':
		hj="select * from diseases where disease_id='%s'"%(d_id)
		data['up']=select(hj)
	if "update" in request.form:
		title=request.form['title']
		description=request.form['descri']
		u="update diseases set title='%s',description='%s' where disease_id='%s'"%(title,description,d_id)
		update(u)
		return redirect(url_for('doctor.admin_view_disease_symptom',d_id=d_id))
	return render_template('admin_view_disease_symptom.html',data=data)

@doctor.route('/admin_manage_symptoms',methods=['get','post'])
def admin_manage_symptoms():
	
	data={}
	d_id=request.args['disease_id']
	q="select * from symptoms where disease_id='%s'"%(d_id) 
	res=select(q)
	data['symptoms']=res
	if 'submit' in request.form:
		sym=request.form['sym']
		d_id=request.args['disease_id']
		# symptoms=request.form['sym']
		# date_time=request.form['dt']

		q="insert into symptoms VALUES(null,'%s','%s')"%(d_id,sym)
		insert(q)
		flash("Added Successfully..")
		return redirect(url_for('doctor.admin_manage_symptoms',disease_id=d_id))
		
	if 'action' in request.args:
			action=request.args['action']
			symptoms_id=request.args['symptoms_id']

	else:
		action=None

	if action=='delete':
		d_id=request.args['disease_id']
		q="delete from symptoms where symptoms_id='%s'"%(symptoms_id)
		delete(q)
	
		flash("Deleted........!")
		return redirect(url_for('doctor.admin_manage_symptoms',disease_id=d_id))

	if action=='update':
		hj="select * from symptoms where symptoms_id='%s'"%(symptoms_id)
		data['up']=select(hj)
	if "update" in request.form:
		sym=request.form['sym']
		d_id=request.args['disease_id']
		
		u="update symptoms  set symptoms='%s' where symptoms_id='%s'"%(sym,symptoms_id)
		update(u)
		return redirect(url_for('doctor.admin_manage_symptoms',disease_id=d_id))

	return render_template('admin_manage_symptoms.html',data=data)



@doctor.route('/doctor_view_patient',methods=['get','post'])
def doctor_view_patient():
	data={}
	# q="SELECT *,appointments.status AS st FROM doctor INNER JOIN hospitals USING(hospital_id) INNER JOIN appointments USING(doctor_id) INNER JOIN patients USING(patient_id) WHERE `appointments`.`status`='appointed'"
	q="select * from patients inner join login using(login_id)"
	res=select(q)
	data['users']=res
	if 'action' in request.args:
		action=request.args['action']
		lid=request.args['lid']
	else:
		action=None
	if action=='delete':
		q="delete from patients where login_id='%s'"%(lid)
		delete(q)
		flash('Deleted Successfully....')
		return redirect(url_for('doctor.doctor_view_patient'))
	return render_template('doc_viewusertoupanddel.html',data=data)


@doctor.route('/updateuserdetails',methods=['get','post'])
def updateuserdetails():
	data={}
	lid=request.args['lid']
	q="select * from patients where login_id='%s'"%(lid)
	data['up']=select(q)
	if 'submit' in request.form:
		fn=request.form['fn']
		ln=request.form['ln']
		place=request.form['Place']
		dob=request.form['dob']
		gen=request.form['gen']
		phone=request.form['phone']
		email=request.form['email']
		q="update patients set first_name='%s',last_name='%s',dob='%s',gender='%s',place='%s',phone='%s',email='%s'"%(fn,ln,place,dob,gen,phone,email)
		update(q)
		flash('Updated Successfully')
		return redirect(url_for(doctor.doctor_view_patient))
	return render_template('updateuserdetails.html',data=data)



# @doctor.route('/doctor_view_test_result')
# def doctor_view_test_result():
# 	return render_template('doctor_view_test_result.html')  


@doctor.route('/doctor_view_test_result')
def doctor_view_test_result():
    data = {}
    did = session['did']  # Assuming doctor's session ID is stored as 'did'

    # Corrected SQL query for fetching doctor-specific test results
    gg = """
    SELECT 
        `test_reult`.*, 
        CONCAT(`patients`.`first_name`, ' ', `patients`.`last_name`) AS patient_name,
        CONCAT(`doctor`.`first_name`, ' ', `doctor`.`last_name`) AS doctor_name,
        `test_reult`.`date` AS test_reult_date,
        `test_reult`.`amount` AS xxx,
        `test_reult`.`status` AS yyy,
        `test_reult`.`time` AS test_reult_time
    FROM 
        `test_reult`
    INNER JOIN `appointments` USING(`appointment_id`)
    INNER JOIN `doctor` USING(`doctor_id`)
    INNER JOIN `patients` USING(`patient_id`)
    WHERE `doctor_id`='%s'
    """ % (did)

    data['results'] = select(gg)

    return render_template('doctor_view_test_result.html', data=data)
