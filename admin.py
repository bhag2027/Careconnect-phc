from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
	return render_template('adminhome.html')

@admin.route('/admin_view_hospital')
def admin_view_hospital():

	data={}

	q="SELECT * FROM `hospitals`"
	res=select(q)
	data['hospitals']=res

	if 'action' in request.args:
		action=request.args['action']
		hid=request.args['hid']
		lid=request.args['lid']
	else:
		action=None

	if action=='approve':
		q="UPDATE `login` SET user_type='hospital' WHERE login_id='%s'"%(lid)
		update(q)
		q1="UPDATE `hospitals` SET STATUS='approved' WHERE hospital_id='%s'"%(hid)
		update(q1)

		return redirect(url_for('admin.admin_view_hospital'))

	if action=='reject':
		q="UPDATE `login` SET user_type='pending' WHERE login_id='%s'"%(lid)
		update(q)
		q1="UPDATE `hospitals` SET STATUS='rejected' WHERE hospital_id='%s'"%(hid)
		update(q1)

		return redirect(url_for('admin.admin_view_hospital'))


	return render_template('admin_view_hospital.html',data=data)

@admin.route('/admin_view_doctor')
def admin_view_doctor():

	data={}
	hid=request.args['hid']
	q="SELECT * FROM `doctor` where hospital_id='%s'"%(hid)
	res=select(q)
	data['doctors']=res
	print(data['doctors'])

	return render_template('admin_view_doctor.html',data=data)

@admin.route('/admin_view_rating')
def admin_view_rating():

	data={}
	did=request.args['did']
	q="SELECT * FROM `rating` inner join patients using(patient_id) where doctor_id='%s'"%(did)
	res=select(q)
	data['rate']=res
	print(data['rate'])

	return render_template('admin_view_rating.html',data=data)

# @admin.route('/admin_view_disease_symptom',methods=['get','post'])
# def admin_view_disease_symptom():

	
# 	data={}
# 	q="select * from diseases " 
# 	res=select(q)
# 	data['diseases']=res
# 	if 'submit' in request.form:
# 		title=request.form['title']
# 		description=request.form['descri']
# 		q="INSERT INTO diseases VALUES(null,'%s','%s')"%(title,description)
# 		insert(q)
# 		flash("Disease added successfully..")
# 		return redirect(url_for('admin.admin_view_disease_symptom'))
		
# 	if 'action' in request.args:
# 			action=request.args['action']
# 			d_id=request.args['disease_id']

# 	else:
# 		action=None

# 	if action=='delete':
# 		q="delete from diseases where disease_id='%s'"%(d_id)
# 		delete(q)
	
# 		flash("Deleted........!")
# 		return redirect(url_for('admin.admin_view_disease_symptom'))

# 	if action=='update':
# 		hj="select * from diseases where disease_id='%s'"%(d_id)
# 		data['up']=select(hj)
# 	if "update" in request.form:
# 		title=request.form['title']
# 		description=request.form['descri']
# 		u="update diseases set title='%s',description='%s' where disease_id='%s'"%(title,description,d_id)
# 		update(u)
# 		return redirect(url_for('admin.admin_view_disease_symptom',d_id=d_id))


# 	return render_template('admin_view_disease_symptom.html',data=data)

# @admin.route('/admin_manage_symptoms',methods=['get','post'])
# def admin_manage_symptoms():
	
# 	data={}
# 	d_id=request.args['disease_id']
# 	q="select * from symptoms where disease_id='%s'"%(d_id) 
# 	res=select(q)
# 	data['symptoms']=res
# 	if 'submit' in request.form:
# 		sym=request.form['sym']
# 		d_id=request.args['disease_id']
# 		# symptoms=request.form['sym']
# 		# date_time=request.form['dt']

# 		q="insert into symptoms VALUES(null,'%s','%s')"%(d_id,sym)
# 		insert(q)
# 		flash("Added Successfully..")
# 		return redirect(url_for('admin.admin_manage_symptoms',disease_id=d_id))
		
# 	if 'action' in request.args:
# 			action=request.args['action']
# 			symptoms_id=request.args['symptoms_id']

# 	else:
# 		action=None

# 	if action=='delete':
# 		d_id=request.args['disease_id']
# 		q="delete from symptoms where symptoms_id='%s'"%(symptoms_id)
# 		delete(q)
	
# 		flash("Deleted........!")
# 		return redirect(url_for('admin.admin_manage_symptoms',disease_id=d_id))

# 	if action=='update':
# 		hj="select * from symptoms where symptoms_id='%s'"%(symptoms_id)
# 		data['up']=select(hj)
# 	if "update" in request.form:
# 		sym=request.form['sym']
# 		d_id=request.args['disease_id']
		
# 		u="update symptoms  set symptoms='%s' where symptoms_id='%s'"%(sym,symptoms_id)
# 		update(u)
# 		return redirect(url_for('admin.admin_manage_symptoms',disease_id=d_id))

# 	return render_template('admin_manage_symptoms.html',data=data)



@admin.route('/admin_view_complaint_sendreply',methods=['get','post'])
def admin_view_complaint_sendreply():
	data={}
	q="SELECT * FROM `complaints` INNER JOIN `patients` USING(`patient_id`) "
	res=select(q)
	data['complaints']=res

	j=0
	for i in range(1,len(res)+1):
		if 'replys'+str(i) in request.form:
			reply=request.form['reply'+str(i)]

			q="UPDATE `complaints` SET `reply`='%s' WHERE `complaint_id`='%s'"%(reply,res[j]['complaint_id'])
			update(q)

			return redirect(url_for("admin.admin_view_complaint_sendreply"))
		j=j+1 

	return render_template('admin_view_complaint_sendreply.html',data=data)
