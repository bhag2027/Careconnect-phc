from flask import *
from database import *


pharmacy=Blueprint('pharmacy',__name__)


@pharmacy.route('/pharmacyhome')
def pharmacyhome():
	return render_template('pharmacyhome.html')

@pharmacy.route('/pharmacy_viewprescition',methods=['get','post'])
def pharmacy_viewprescition():
	data={}
	q="SELECT *,CONCAT(`patients`.`first_name` , ' ' , `patients`.`last_name` )  AS patients_name , CONCAT(`doctor`.`first_name` , ' ' , `doctor`.`last_name`) AS doctor_name  FROM  prescription INNER JOIN  `appointments` USING(`appointment_id`) INNER JOIN `doctor` USING(`doctor_id`) INNER JOIN `patients` USING(`patient_id`)  "
	res=select(q)
	data['view']=res
	j=0
	for i in range(1,len(res)+1):
		if 'replys'+str(i) in request.form:
			reply=request.form['reply'+str(i)]

			q="UPDATE `prescription` SET `amount`='%s' WHERE `prescription_id`='%s'"%(reply,res[j]['prescription_id'])
			update(q)

			return redirect(url_for("pharmacy.pharmacy_viewprescition"))
		j=j+1 

	return render_template('pharmacy_viewprescition.html',data=data)


@pharmacy.route('/pharmacypayment')
def pharmacypayment():
	data={}
	aid=request.args['aid']
	q="select * from payment where type='pharmacyfee' and appointment_id='%s'"%(aid)
	data['view']=select(q)
	print(data['view'])
	return render_template('pharmacy_viewpayment.html',data=data)











