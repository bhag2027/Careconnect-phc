from flask import *
from database import *
import uuid

lab=Blueprint('lab',__name__)

@lab.route('/lab_home')
def lab_home():
	return render_template('lab_home.html')  

@lab.route('/lab_view_tequest',methods=['get','post'])
def lab_view_tequest():
	data={}
	hh="SELECT *,CONCAT(`patients`.`first_name`,' ',`patients`.`last_name`) AS patient_name,CONCAT(`doctor`.`first_name`,' ',`doctor`.`last_name`) AS doctor_name ,`test_reult`.`amount`AS xxx FROM test_reult INNER JOIN `appointments`USING(`appointment_id`) INNER JOIN doctor USING(`doctor_id`)INNER JOIN `patients`USING(`patient_id`)"
	data['view']=select(hh)
	res=select(hh)
	j=0
	for i in range(1,len(res)+1):
		if 'replys'+str(i) in request.form:
			reply=request.form['reply'+str(i)]

			q="UPDATE `test_reult` SET `amount`='%s' WHERE `test_reult_id`='%s'"%(reply,res[j]['test_reult_id'])
			update(q)

			return redirect(url_for("lab.lab_view_tequest"))
		j=j+1 
	return render_template('lab_view_tequest.html',data=data) 

@lab.route('/lab_view_medical_report')
def lab_view_medical_report():
	data={}
	patient_id=request.args['patient_id']
	hh="SELECT * FROM `medical_records`INNER JOIN `doctor`USING(`doctor_id`) WHERE `patient_id`='%s'"%(patient_id)
	data['view']=select(hh)
	return render_template('lab_view_medical_report.html',data=data)  

from werkzeug.utils import secure_filename
import uuid
import os

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@lab.route('/lab_add_test_result', methods=['GET', 'POST'])
def lab_add_test_result():
    data = {}
    appointment_id = request.args['appointment_id']

    if 'submit' in request.form:
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = "static/uploads/" + str(uuid.uuid4()) + "_" + filename
            file.save(path)

            # Save file path in DB
            kk = "UPDATE test_reult SET date=CURDATE(), time=CURTIME(), result='%s' WHERE appointment_id='%s'" % (path, appointment_id)
            update(kk)

            flash("Result uploaded successfully.")
            return redirect(url_for('lab.lab_view_tequest'))
        else:
            flash("Only PDF files are allowed.")
            return redirect(url_for('lab.lab_add_test_result', appointment_id=appointment_id))

    return render_template('lab_add_test_result.html', appointment_id=appointment_id, data=data)