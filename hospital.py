from flask import *
from database import *
import uuid
from werkzeug.security import generate_password_hash
from flask import Flask, request, jsonify
from datetime import datetime
hospital=Blueprint('hospital',__name__)

@hospital.route('/hospitalhome')
def hospitalhome():
	return render_template('hospitalhome.html')




@hospital.route('/submit_leave', methods=['POST'])
def submit_leave():
    try:
        doctor_id = request.form.get('doctor_id')
        leave_date = request.form.get('leave_date')

        if not doctor_id or not leave_date:
            return jsonify({'status': 'error', 'message': 'Doctor ID and Leave Date are required'}), 400

        # Ensure doctor_id is an integer
        try:
            doctor_id = int(doctor_id)
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid Doctor ID'}), 400

        # Validate leave_date format
        try:
            parsed_date = datetime.strptime(leave_date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid date format (YYYY-MM-DD required)'}), 400

        # Insert leave request into DB
        query = "INSERT INTO leave_request (doctor_id, leave_date) VALUES (%s, %s)"
        insert(query, (doctor_id, parsed_date))

        return jsonify({'status': 'success', 'message': 'Leave request submitted', 'doctor_id': doctor_id, 'leave_date': leave_date})

    except Exception as e:
        print("Server Error:", str(e))  # Logs error in Flask console
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500










@hospital.route('/hospitals_view_patients')
def hospitals_view_patients():
    data = {}

   
    q = "SELECT * FROM `patients`"
    res = select(q)
    data['patients'] = res

   
    if 'action' in request.args:
        action = request.args['action']
        patient_name = request.args.get('patient_name')  # Use `.get()` to prevent KeyError

        if action == 'delete':
            # Optional: Delete related records first
            q1 = "DELETE FROM appointments WHERE patient_id IN (SELECT patient_id FROM patients WHERE first_name='%s')" % (patient_name)
            delete(q1)

            # Delete the patient
            q2 = "DELETE FROM patients WHERE first_name='%s'" % (patient_name)
            delete(q2)

            flash(f"Patient '{patient_name}' deleted successfully!", "success")
            return redirect(url_for('hospital.hospitals_view_patients'))

    return render_template('hospitals_view_patients.html', data=data)


@hospital.route('/hospitals_view_appointment')
def hospitals_view_appointment():
	data={}
	q="SELECT *,CONCAT(`patients`.`first_name`,' ',`patients`.`last_name`) AS patient_name,CONCAT(`doctor`.`first_name`,' ',`doctor`.`last_name`) AS doctor_name FROM `appointments` INNER JOIN `doctor` USING (doctor_id) INNER JOIN patients USING(patient_id) WHERE  hospital_id='%s'"%(session['hid'])
	res=select(q)
	data['appoinment']=res
	if 'action' in request.args:
		action=request.args['action']
		appointment_id=request.args['appointment_id']
		if action=='accept':
			q="update appointments set status='appointed' where appointment_id='%s'"%(appointment_id)
			update(q)
			print(q)
			flash("Appointed succesfully")
			return redirect(url_for('hospital.hospitals_view_appointment'))

		if action=='reject':
			q="update appointments set status='cancelled' where appointment_id='%s'"%(appointment_id)
			update(q)
			flash("Rejected succesfully")
			return redirect(url_for('hospital.hospitals_view_appointment'))

	return render_template('hospitals_view_appointment.html',data=data)






@hospital.route('/hospital_manage_departments',methods=['get','post'])
def hospital_manage_departments():
	data={}	
	hid=session['hid']	
	q="SELECT * FROM `departments` WHERE `hospital_id`='%s'"%(hid)
	data['department']=select(q)
	if 'submit' in request.form:
		dname=request.form['dname']
		q="INSERT INTO `departments`(`hospital_id`,`department_name`)VALUES('%s','%s')"%(session['hid'],dname)
		insert(q)
		flash("ADDED")
		return redirect(url_for('hospital.hospital_manage_departments'))
	return render_template('hospital_manage_departments.html',data=data)

@hospital.route('/hospital_managedoctors', methods=['get', 'post'])
def hospital_managedoctors():
    data = {}
    
    # Fetch department details
    w = "SELECT * FROM departments WHERE hospital_id='%s'" % (session['hid'])
    data['ww'] = select(w)
    
    # Fetch doctor details
    q = "SELECT * FROM `doctor` WHERE hospital_id='%s'" % (session['hid'])
    res = select(q)
    data['doctors'] = res

    # Fetch department details again (unnecessary duplicate query removed)
    data['dept'] = data['ww']  
    if 'mmm' in request.form:
        doctor_id = request.form.get('doctor_id')
        leave_date = request.form.get('leave_date')
        query = "INSERT INTO leave_request  VALUES (null,'%s', '%s')"%(doctor_id, leave_date)
        insert(query)
        flash("Leave  submitted")
        return redirect(url_for('hospital.hospital_managedoctors'))
    # Doctor registration logic
    if 'submit' in request.form:
        uname = request.form['uname']
        passs = request.form['pword']
        hashed_pwd = generate_password_hash(passs)

        fname = request.form['fname']
        lname = request.form['lname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']
        quali = request.form['qualification']
        photo = request.files['photo']
        dep = request.form['dep']

        # Save photo with unique filename
        path = "static/images/" + str(uuid.uuid4()) + photo.filename
        photo.save(path)

        # Insert into login and doctor tables
        q = "INSERT INTO login(`username`, `password`, `user_type`) VALUES ('%s', '%s', 'doctor')" % (uname, hashed_pwd)
        id = insert(q)
        q1 = "INSERT INTO `doctor` VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            id, session['hid'], fname, lname, place, phone, email, path, quali, dep)
        insert(q1)

        flash("REGISTERED SUCCESSFULLY")
        return redirect(url_for('hospital.hospital_managedoctors'))

    # Action Handling (delete/update)
    action = request.args.get('action')  # Use .get() for safer retrieval
    did = request.args.get('did')        # Use .get() for safer retrieval
    lid = request.args.get('lid')        # Use .get() for safer retrieval

    if action == 'delete':
        if did and lid:  # Ensure both doctor_id and login_id exist
            q = "DELETE FROM doctor WHERE doctor_id='%s'" % (did)
            delete(q)
            w = "DELETE FROM login WHERE login_id='%s'" % (lid)
            delete(w)
            flash("DELETED SUCCESSFULLY...")
        else:
            flash("Error: Missing Doctor or Login ID.")
        return redirect(url_for('hospital.hospital_managedoctors'))

    if action == 'update':
        if did:
            e = "SELECT * FROM doctor WHERE doctor_id='%s'" % (did)
            data['up'] = select(e)
        else:
            flash("Error: Doctor ID is missing.")

    # Doctor update logic
    if 'update' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']
        quali = request.form['qualification']
        dep = request.form['dep']

        if all([fname, lname, place, phone, email, quali, dep, did]):  # Ensure all fields are filled
            q = """
            UPDATE doctor 
            SET 
                first_name='%s',
                last_name='%s',
                place='%s',
                phone='%s',
                email='%s',
                qualification='%s',
                department='%s' 
            WHERE doctor_id='%s'
            """ % (fname, lname, place, phone, email, quali, dep, did)
            
            update(q)
            flash("UPDATED SUCCESSFULLY...")
        else:
            flash("All fields are required for updating doctor details.")
            
        return redirect(url_for('hospital.hospital_managedoctors'))

    return render_template('hospitals_managedoctors.html', data=data)

@hospital.route('/hospital_mark_leave', methods=['POST'])
def hospital_mark_leave():
    did = request.form.get('doctor_id')
    leave_date = request.form.get('leave_date')

    print("Leave API hit - Doctor ID:", did, "Date:", leave_date)

    if did and leave_date:
        check_leave = "SELECT * FROM doctor_leave WHERE doctor_id=%s AND leave_date=%s"
        leave_res = select(check_leave, (did, leave_date))

        print("Existing Leave Check:", leave_res)

        if leave_res:
            return jsonify({"status": "error", "message": "Doctor is already on leave for this date."})
        else:
            insert_query = "INSERT INTO doctor_leave (doctor_id, leave_date) VALUES (%s, %s)"
            insert(insert_query, (did, leave_date))

            print("Leave Added Successfully!")
            return jsonify({"status": "success", "message": "Leave marked successfully!"})

    return jsonify({"status": "error", "message": "Invalid request!"})
@hospital.route('/hospital_manage_shedule', methods=['get', 'post'])
def hospital_manage_shedule():
    data = {}
    did = request.args.get('did')
    data['did'] = did

    # Fetch existing schedule details
    q = "SELECT scheduling_id, ftime, ttime FROM scheduling WHERE doctor_id='%s'" % (did)
    data['shedule'] = select(q)

    # Add schedule logic
    if 'submit' in request.form:
        ftime = request.form['ft']
        ftime_ampm = request.form['ft_ampm']
        ttime = request.form['tt']
        ttime_ampm = request.form['tt_ampm']

        full_ftime = f"{ftime} {ftime_ampm}"
        full_ttime = f"{ttime} {ttime_ampm}"

        q = "INSERT INTO `scheduling`(`doctor_id`, `ftime`, `ttime`) VALUES ('%s', '%s', '%s')" % (did, full_ftime, full_ttime)
        insert(q)
        flash("Schedule Added Successfully")
        return redirect(url_for('hospital.hospital_manage_shedule', did=did))

    # Update logic
    action = request.args.get('action')
    shid = request.args.get('shid')

    if action == 'update':
        e = "SELECT * FROM scheduling WHERE scheduling_id='%s'" % (shid)
        data['up'] = select(e)

    if 'update' in request.form:
        ftime = request.form['ft']
        ftime_ampm = request.form['ft_ampm']
        ttime = request.form['tt']
        ttime_ampm = request.form['tt_ampm']

        full_ftime = f"{ftime} {ftime_ampm}"
        full_ttime = f"{ttime} {ttime_ampm}"

        q = "UPDATE `scheduling` SET `ftime`='%s', `ttime`='%s' WHERE `scheduling_id`='%s'" % (full_ftime, full_ttime, shid)
        update(q)
        flash("Schedule Updated Successfully")
        return redirect(url_for('hospital.hospital_manage_shedule', did=did))

    return render_template('hospital_manage_shedule.html', data=data)



    # Update schedule logic
    action = request.args.get('action')
    shid = request.args.get('shid')  # Schedule ID

    if action == 'update':
        e = "SELECT * FROM scheduling WHERE scheduling_id='%s'" % (shid)
        data['up'] = select(e)

    if 'update' in request.form:
        # Get updated time and AM/PM values
        ftime = request.form['ft']
        ftime_ampm = request.form['ft_ampm']

        # Combine the time values with AM/PM
        full_ftime = f"{ftime} {ftime_ampm}"

        # Update the schedule with the new time
        q = "UPDATE `scheduling` SET `ftime`='%s' WHERE `scheduling_id`='%s'" % (full_ftime, shid)
        update(q)
        flash("Schedule Updated Successfully")
        return redirect(url_for('hospital.hospital_manage_shedule', did=did))

    return render_template('hospital_manage_shedule.html', data=data)



    # Delete schedule logic
    if action == 'delete':
        q = "DELETE FROM scheduling WHERE scheduling_id='%s'" % (shid)
        delete(q)
        flash("Schedule Deleted Successfully")
        return redirect(url_for('hospital.hospital_manage_shedule', did=did))

    return render_template('hospital_manage_shedule.html', data=data)


# from datetime import datetime, timedelta

# def add_minutes(time_str, minutes):
#     """
#     Adds minutes to a time string in the format 'HH:MM'.
#     """
#     time_format = "%H:%M"
#     time_obj = datetime.strptime(time_str, time_format)
#     new_time_obj = time_obj + timedelta(minutes=minutes)
#     return new_time_obj.strftime(time_format)

# @hospital.route('add_minutes')
# def add_minutes_filter(time_str, minutes):
#     return add_minutes(time_str, minutes)


@hospital.route('/hospital_blood_donationcamp',methods=['get','post'])
def hospital_blood_donationcamp():
	data={}
	q="SELECT * FROM `blooddonation`"  
	res=select(q)
	data['view']=res

	if 'submit' in request.form:
		place=request.form['place']
		date=request.form['date']
		ft=request.form['ft']
		tt=request.form['tt']
		q="insert into blooddonation values(null,'%s','%s','%s','%s')"%(place,date,ft,tt)
		insert(q)
		flash("ADD SUCCEFULLY...")
		return redirect(url_for('hospital.hospital_blood_donationcamp'))
	if 'action' in request.args:
		action=request.args['action']
		b_id=request.args['b_id']
	else:
		action=None
	if action=='delete':
			q="delete from blooddonation where blooddonation_id='%s'"%(b_id)
			delete(q)
			flash("Deleted succesfully")
			return redirect(url_for('hospital.hospital_blood_donationcamp'))
	if action=='update':
			r="select * from blooddonation where blooddonation_id='%s'"%(b_id)
			data['up']=select(r)
	if 'update' in request.form: 
		place=request.form['place']
		date=request.form['date']
		ft=request.form['ft']
		tt=request.form['tt']
		q="update blooddonation set place='%s',date='%s', fromtime='%s',tofrom='%s' where blooddonation_id='%s'"%(place,date,ft,tt,b_id)
		update(q)
		flash("UPDATED SUCCEFULLY...")
		return redirect(url_for('hospital.hospital_blood_donationcamp'))


	return render_template('hospital_blood_donationcamp.html',data=data)



@hospital.route('/hospital_managelab',methods=['get','post'])
def hospital_managelab():

	data={}

	q="SELECT * FROM `lab`"  
	res=select(q)
	data['lab']=res

	# q="SELECT * FROM `departments`"
	# res=select(q)
	# data['dept']=res

	if 'submit' in request.form:
		name=request.form['name']
		detail=request.form['detail']
		uname=request.form['uname']
		pwd=request.form['pwd']
		hashed_pwd = generate_password_hash(pwd)
		ss="insert into login values(null,'%s','%s','lab')"%(uname,hashed_pwd)
		zz=insert(ss)
		q1="INSERT INTO `lab` VALUES(null,'%s','%s','%s','%s')"%(zz,session['hid'],name,detail)
		insert(q1)
		flash("Added Successfully.....")
		return redirect(url_for('hospital.hospital_managelab'))
	
	if 'action' in request.args:
		action=request.args['action']
		lid=request.args['lid']
	else:
		action=None
	if action == 'delete':
		q="delete from lab where lab_id='%s'"%(lid)
		delete(q)
		flash("DELETED SUCCEFULLY...")
		return redirect(url_for('hospital.hospital_managelab'))
	if action == 'update':
		e="select * from lab where lab_id='%s'"%(lid)
		data['up']=select(e)
	if 'update' in request.form:
		name=request.form['name']
		detail=request.form['detail']

		q="update lab set name='%s',details='%s' where lab_id='%s'"%(name,detail,lid)
		update(q)
		flash("UPDATED SUCCEFULLY...")
		return redirect(url_for('hospital.hospital_managelab'))
	return render_template('hospital_manage_lab.html',data=data)



@hospital.route('/hospital_manageambulance',methods=['get','post'])
def hospital_manageambulance():

	data={}

	q="SELECT * FROM `ambulance`"  
	res=select(q)
	data['lab']=res

	# q="SELECT * FROM `departments`"
	# res=select(q)
	# data['dept']=res

	if 'submit' in request.form:
		name=request.form['name']
		detail=request.form['detail']
		phone=request.form['phone']
		reg=request.form['reg']
		q1="INSERT INTO `ambulance` VALUES(null,'%s','%s','%s','%s','%s')"%(session['hid'],name,detail,phone,reg)
		insert(q1)
		flash("Added Successfully.....")
		return redirect(url_for('hospital.hospital_manageambulance'))
	
	if 'action' in request.args:
		action=request.args['action']
		aid=request.args['aid']
	else:
		action=None
	if action == 'delete':
		q="delete from ambulance where Ambulance_id='%s'"%(aid)
		delete(q)
		flash("DELETED SUCCEFULLY...")
		return redirect(url_for('hospital.hospital_manageambulance'))
	if action == 'update':
		e="select * from ambulance where Ambulance_id='%s'"%(aid)
		data['up']=select(e)
	if 'update' in request.form:
		name=request.form['name']
		detail=request.form['detail']
		phone=request.form['phone']
		reg=request.form['reg']

		q="update ambulance set Ambulance='%s',Details='%s',phone='%s',Regnum='%s'"%(name,detail,phone,reg)
		update(q)
		flash("UPDATED SUCCEFULLY...")
		return redirect(url_for('hospital.hospital_manageambulance'))
	return render_template('hospital_manageambulance.html',data=data)



