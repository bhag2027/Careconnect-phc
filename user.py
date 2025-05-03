from flask import *
from database import *

user=Blueprint('user',__name__)

@user.route('/user_home')
def user_home():
	return render_template('user_home.html') 


@user.route('/user_view_doctors')
def user_view_doctors():
	data={}
    
	vv="select * from doctor"
	data['doctor']=select(vv)
	return render_template('user_view_doctors.html',data=data) 



@user.route('/user_view_schedule', methods=['GET', 'POST'])
def user_view_schedule():
    data = {}
    did = request.args.get('did')  # Get doctor ID
    bb = ""

    if not did:
        flash("Doctor ID is missing.")
        return redirect(url_for('user.user_view_doctors'))

    booked_slots = []  # Store booked time slots

    # Fetch all leave dates for this doctor
    leave_query = "SELECT date FROM leave_request WHERE doctor_id='%s'" % (did)
    leave_data = select(leave_query)
    leave_dates = [str(row['date']) for row in leave_data]  # Convert to list

    if request.method == 'POST' and 'date' in request.form:
        bb = request.form['date']

        # Check if doctor is on leave
        if bb in leave_dates:
            flash("Doctor is not available on this date.")
            return redirect(url_for('user.user_view_schedule', did=did))

        # Fetch booked appointments for the selected date
        appointment_query = "SELECT time FROM appointments WHERE appointment_date='%s' AND doctor_id='%s'" % (bb, did)
        booked_data = select(appointment_query)

        # Extract booked times
        booked_slots = [row['time'] for row in booked_data]

    # Fetch doctor's schedule
    schedule_query = "SELECT * FROM scheduling WHERE doctor_id='%s'" % (did)
    schedule_data = select(schedule_query)

    # Add "is_booked" status to each schedule slot
    for row in schedule_data:
        row['is_booked'] = row['ftime'] in booked_slots

    data['view'] = schedule_data
    data['selected_date'] = bb

    return render_template('user_view_schedule.html', data=data, bb=bb, did=did, leave_dates=leave_dates)



# @user.route('/user_book_appointment',methods=['get','post'])
# def user_book_appointment():
# 	data={}
# 	did=request.args['did']
# 	if 'submit' in request.form:
# 		date=request.form['date']
# 		time=request.form['time']
# 		pp="SELECT * FROM `appointments`WHERE `appointment_date`='%s' and time='%s'"%(date,time)
# 		nn=select(pp)
# 		tt="SELECT * FROM `scheduling` WHERE '%s' BETWEEN `ftime` AND `ttime`"%(time)
# 		vv=select(tt)
# 		if nn or vv:
# 			flash("This time slot is already booked, and the doctor is not available.")
# 			return redirect(url_for('user.user_book_appointment',did=did))
# 		else:
# 			token="SELECT * FROM `appointments`WHERE `appointment_date`='%s' ORDER BY `appointment_id`"%(date)
# 			cc=select(token)
# 			if cc:
# 				ccc=cc[-1]['token_no']
# 				token_no=int(ccc)+1
# 			else:
# 				token_no=1
# 			hh="insert into appointments values (null,'%s','%s','%s','%s','paid','5','%s')"%(did,session['pid'],date,time,token_no)
# 			dd=insert(hh)
# 			return redirect(url_for('user.user_payment_appointment',dd=dd))
# 	mm="select * from appointments where patient_id='%s'"%(session['pid'])
# 	data['view']=select(mm)
# 	return render_template('user_book_appointment.html',data=data,did=did) 


@user.route('/user_view_medical_report')
def user_view_medical_report():
	data={}
	hh="SELECT * FROM `medical_records`INNER JOIN `doctor`USING(`doctor_id`) WHERE `patient_id`='%s'"%(session['pid'])
	data['view']=select(hh)
	return render_template('user_view_medical_report.html',data=data) 


@user.route('/user_view_test_result')
def user_view_test_result():
	data={}
	gg="SELECT *,CONCAT(`patients`.`first_name`,' ',`patients`.`last_name`) AS patient_name,CONCAT(`doctor`.`first_name`,' ',`doctor`.`last_name`) AS doctor_name,`test_reult`.`date`AS test_reult_date ,`test_reult`.`amount`AS xxx ,`test_reult`.`status`AS yyy ,`test_reult`.`time` AS test_reult_time FROM test_reult INNER JOIN `appointments`USING(`appointment_id`) INNER JOIN doctor USING(`doctor_id`)INNER JOIN `patients`USING(`patient_id`) WHERE `patient_id`='%s'"%(session['pid'])
	data['view']=select(gg)
	return render_template('user_view_test_result.html',data=data) 


@user.route('/user_chat_with_doctor',methods=['get','post'])
def user_chat_with_doctor():
	data={}
 
	did=request.args['did']
	data['did']=session['lid']
	receiver="select * from doctor where doctor_id='%s'"%(did)
	vvv=select(receiver)
	receiver_id=vvv[0]['login_id']
 
	pid=session['pid']
	data['pid']=session['lid']
	name=request.args['name']
	data['name']=name
	q="select * from messages where (sender_id='%s' and receiver_id='%s') or (sender_id='%s' and receiver_id='%s') "%(receiver_id,session['lid'],session['lid'],receiver_id)
	res=select(q)
	print(res)
	data['chat']=res
	if 'submit' in request.form:
		msg=request.form['msg']
		q="insert into messages value(NULL,'%s','patient','%s','doctor','%s',NOW())"%(session['lid'],receiver_id,msg)
		insert(q)
		return redirect(url_for('user.user_chat_with_doctor',name=name,did=did)) 

	return render_template('user_chat_with_doctor.html',data=data) 


# @user.route('/user_view_priscription')
# def user_view_priscription():
# 	data={}
# 	hh="SELECT *,`prescription`.`status`AS ddd FROM `prescription`INNER JOIN `appointments`USING(`appointment_id`) WHERE `patient_id`='%s' "%(session['pid'])
# 	data['view']=select(hh)
# 	return render_template('user_view_priscription.html',data=data) 


@user.route('/user_view_priscription')
def user_view_priscription():
    data = {}
    hh = """
        SELECT `prescription`.*, `prescription`.`status` AS ddd, 
        CONCAT(`doctor`.`first_name`, ' ', `doctor`.`last_name`) AS doctor_name
        FROM `prescription`
        INNER JOIN `appointments` USING(`appointment_id`)
        INNER JOIN `doctor` ON `appointments`.`doctor_id` = `doctor`.`doctor_id`
        WHERE `patient_id`='%s'
    """ % (session['pid'])
    
    data['view'] = select(hh)
    return render_template('user_view_priscription.html', data=data)


# @user.route('/user_prescription_payment',methods=['get','post'])
# def user_prescription_payment():
# 	amount=request.args['amount']
# 	prescription_id=request.args['prescription_id']
# 	if 'btn' in request.form:
# 		hjh="update test_reult set status='paid' where test_reult_id='%s'"%(prescription_id)
# 		update(hjh)
# 		flash("payment success........!")
# 		return redirect(url_for('user.user_view_test_result'))
# 	return render_template('user_prescription_payment.html',amount=amount) 

@user.route('/user_prescription_payment', methods=['get', 'post'])
def user_prescription_payment():
    amount = request.args['amount']
    prescription_id = request.args['prescription_id']
    
    if 'btn' in request.form:
        # Correcting the table name and updating 'payment_status'
        update_query = """
            UPDATE `test_reult`
            SET `status` = 'paid'
            WHERE `test_reult_id` = '%s'
        """ % (prescription_id)
        
        update(update_query)
        flash("Payment successful...!")
        return redirect(url_for('user.user_view_test_result'))
    
    return render_template('user_prescription_payment.html', amount=amount)



@user.route('/user_payment_appointment', methods=['GET', 'POST'])
def user_payment_appointment():
    did = request.args.get('did')  # Get doctor ID from URL

    if not did:
        flash("Doctor ID is missing!", "error")
        return redirect(url_for('user.user_view_doctors'))  # Redirect to doctor list if ID is missing

    if 'btn' in request.form:
        hjh = "INSERT INTO payment VALUES (NULL, '%s', '5', CURDATE(), 'success')" % (did)
        insert(hjh)
        flash("APPOINTMENT SUCCESS........!")

        # ✅ Pass the doctor ID when redirecting to 'user_view_schedule'
        return redirect(url_for('user.user_view_schedule', did=did))

    return render_template('user_payment_appointment.html', did=did)  # Pass 'did' to template




@user.route('/user_view_appointment')
def useuser_view_appointmentr_home():
	data={}
	jj="SELECT * FROM `appointments`INNER JOIN `doctor`USING(`doctor_id`) WHERE `patient_id`='%s'"%(session['pid'])
	data['view']=select(jj)
	return render_template('user_view_appointment.html',data=data) 



# from datetime import datetime

# @user.route('/user_book_appointment', methods=['GET', 'POST'])
# def user_book_appointment():
#     data = {}
#     did = request.args['did']

#     # Fetch the doctor's available time range from the database
#     doctor_time_query = "SELECT ftime, ttime FROM scheduling WHERE doctor_id='%s'" % (did)
#     doctor_schedule = select(doctor_time_query)
    
#     if not doctor_schedule:
#         flash("Doctor schedule not found.")
#         return redirect(url_for('user.user_book_appointment'))

#     ftime = doctor_schedule[0]['ftime']
#     ttime = doctor_schedule[0]['ttime']

#     if 'submit' in request.form:
#         # date = request.form['date']
#         time = request.form['time']

#         # Check if the selected time is within the doctor's available time range
#         selected_time = datetime.strptime(time, '%H:%M')
#         available_from_time = datetime.strptime(ftime, '%H:%M')
#         available_to_time = datetime.strptime(ttime, '%H:%M')

#         if not (available_from_time <= selected_time <= available_to_time):
#             flash("The doctor is not available at this time.")
#             return redirect(url_for('user.user_book_appointment', did=did))

#         # Check if the selected time slot is already booked
#         token_query = "SELECT * FROM `appointments` WHERE `appointment_date`='%s' AND `time`='%s' ORDER BY `appointment_id`" % (date, time)
#         existing_appointments = select(token_query)

#         if existing_appointments:
#             flash("The doctor is already booked at this time.")
#             return redirect(url_for('user.user_book_appointment', did=did))

#         # Generate a new token number
#         if existing_appointments:
#             last_appointment = existing_appointments[-1]
#             token_no = int(last_appointment['token_no']) + 1
#         else:
#             token_no = 1

#         # Insert the new appointment
#         insert_query = "INSERT INTO appointments (doctor_id, patient_id, appointment_date, time, status,amount, token_no) VALUES ('%s', '%s', curdate(), '%s', 'paid', '0','%s')" % (did, session['pid'], date, time, token_no)
#         insert(insert_query)

#         # Redirect to the payment page for the appointment
#         return redirect(url_for('user.user_payment_appointment', dd=token_no))

#     # Fetch user's previous appointments
#     user_appointments_query = "SELECT * FROM appointments WHERE patient_id='%s'" % (session['pid'])
#     data['view'] = select(user_appointments_query)

#     return render_template('user_book_appointment.html', data=data, did=did)





from datetime import datetime

@user.route('/user_book_appointment', methods=['GET', 'POST'])
def user_book_appointment():
    data = {}
    did = request.args['did']
    date = request.args['date']
    ftime = request.args['ftime']

    # Fetch the doctor's available time range
    doctor_time_query = "SELECT ftime, ttime FROM scheduling WHERE doctor_id='%s'" % did
    doctor_schedule = select(doctor_time_query)

    if not doctor_schedule:
        flash("Doctor schedule not found.")
        return redirect(url_for('user.user_view_schedule'))

    ftime_str = doctor_schedule[0].get('ftime')
    ttime_str = doctor_schedule[0].get('ttime')

    # ✅ Check if time values are missing
    if not ftime_str or not ttime_str:
        flash("Doctor's available time is not properly set. Please contact admin.")
        return redirect(url_for('user.user_view_schedule'))

    try:
        available_from_time = datetime.strptime(ftime_str, '%I:%M %p')  # 12-hour format with AM/PM
        available_to_time = datetime.strptime(ttime_str, '%I:%M %p')
        selected_time = datetime.strptime(ftime, '%I:%M %p')
    except ValueError:
        flash("Invalid time format in database.")
        return redirect(url_for('user.user_view_schedule'))

    # Optional: Time range validation
    # if not (available_from_time <= selected_time <= available_to_time):
    #     flash("The doctor is not available at this time.")
    #     return redirect(url_for('user.user_view_schedule', did=did))

    if 'submit' in request.form:
        type = request.form['type']

        # Check if slot already booked
        token_query = """SELECT * FROM `appointments` 
                         WHERE `appointment_date`='%s'  
                         AND `doctor_id`='%s' 
                         AND `time`='%s'""" % (date, did, ftime)
        existing_appointments = select(token_query)

        if existing_appointments:
            flash("This time slot is already booked. Please choose another time.")
            return redirect(url_for('user.user_view_schedule', did=did))

        # Generate token number
        token_query = """SELECT MAX(token_no) as max_token FROM appointments 
                         WHERE `doctor_id`='%s' AND `appointment_date`='%s'""" % (did, date)
        existing_tokens = select(token_query)

        token_no = int(existing_tokens[0]['max_token']) + 1 if existing_tokens and existing_tokens[0]['max_token'] else 1

        # Insert appointment
        insert_query = """INSERT INTO appointments 
                          (doctor_id, patient_id, appointment_date, time, status, amount, token_no, type) 
                          VALUES ('%s', '%s', '%s', '%s', 'paid', '5', '%s', '%s')""" % (
                            did, session['pid'], date, ftime, token_no, type)
        insert(insert_query)

        return redirect(url_for('user.user_payment_appointment', did=did))

    # Load past appointments
    user_appointments_query = "SELECT * FROM appointments WHERE patient_id='%s'" % session['pid']
    data['view'] = select(user_appointments_query)

    return render_template('user_book_appointment.html', data=data, did=did, date=date)


@user.route('/user_send_complaints', methods=['GET', 'POST'])
def user_send_complaints():
    data = {}
    
    # Fetch complaints for the current patient with date and time
    q = "SELECT * FROM `complaints` WHERE patient_id = '%s'" % (session['pid'])
    print(q, "pp")
    res = select(q)
    data['view'] = res

    # Insert complaint with current date and time
    if 'submit' in request.form:
        com = request.form['com']
        q = "INSERT INTO `complaints` VALUES(NULL, '%s', '%s', 'pending', NOW())" % (session['pid'], com)
        insert(q)
        return redirect(url_for('user.user_send_complaints'))
    
    return render_template('user_send_complaints.html', data=data)



