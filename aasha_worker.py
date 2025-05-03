from flask import *
from database import *

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

aasha_worker = Blueprint('aasha_worker', __name__)

@aasha_worker.route('/aasha_worker_home')
def aasha_worker_home():
    return render_template('aasha_worker_home.html') 


@aasha_worker.route('/aasa_worker_send_Emergency', methods=['GET', 'POST'])
def aasa_worker_send_Emergency():
	if request.method == 'POST':  
		message = request.form['message']

		hh = "SELECT * FROM patients"
		xx = select(hh)

		sender_email = "annaeldho4@gmail.com"  
		sender_password = "fvhj ykzo epra turg" 

		subject = "Emergency Alert from PHC"

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(sender_email, sender_password)

		for i in xx:
			receiver_email = i['email']

			# Create email content
			msg = MIMEMultipart()
			msg['From'] = sender_email
			msg['To'] = receiver_email
			msg['Subject'] = subject
			msg.attach(MIMEText(message, 'plain'))

			server.sendmail(sender_email, receiver_email, msg.as_string())

		server.quit()
		flash("Emergency message sent successfully!", "success")
	data={}
	return render_template('aasa_worker_send_Emergency.html',data=data)

from datetime import datetime
from datetime import datetime

@aasha_worker.route('/aasha_worker_add_event', methods=['GET', 'POST'])
def aasha_worker_add_event():
    data = {}
    event_data = None  # Store event details if editing

    if request.method == 'POST':  
        event_id = request.form.get('event_id')  # Get event_id if editing
        event = request.form['event']
        description = request.form['description']
        date = request.form['dd']
        time = request.form['tt']
        ampm = request.form['ampm']

        # Convert time to 24-hour format
        time_24hr = datetime.strptime(f"{time} {ampm}", "%I:%M %p").strftime("%H:%M:%S")

        if event_id:  
            # Update existing event
            query = "UPDATE event SET event='%s', description='%s', date='%s', time='%s' WHERE event_id='%s'" % (
                event, description, date, time_24hr, event_id
            )
            update(query)
            flash("Event updated successfully!")
        else:
            # Insert new event
            query = "INSERT INTO event VALUES (NULL, '%s', '%s', '%s', '%s', '%s')" % (
                session['aasha_worker'], event, description, date, time_24hr
            )
            insert(query)
            flash("Event added successfully!")

        return redirect(url_for('aasha_worker.aasha_worker_add_event'))

    # Check if user is editing an event
    event_id = request.args.get('edit_event_id')
    if event_id:
        query = "SELECT * FROM event WHERE event_id='%s'" % event_id
        result = select(query)
        if result:
            event_data = result[0]
            event_data['time'] = datetime.strptime(event_data['time'], "%H:%M:%S").strftime("%I:%M %p")  # Convert to 12-hour format

    # Fetch existing events
    query = "SELECT * FROM event WHERE aasha_worker_id='%s'" % (session['aasha_worker'])
    events = select(query)

    # Convert time from 24-hour format to 12-hour format with AM/PM
    for row in events:
        try:
            row['time'] = datetime.strptime(str(row['time']), "%H:%M:%S").strftime("%I:%M %p")
        except ValueError:
            row['time'] = str(row['time'])  # Keep original if conversion fails

    data['view'] = events
    data['edit_event'] = event_data  # Send event details if editing

    return render_template('aasha_worker_add_event.html', data=data)



@aasha_worker.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    query = "DELETE FROM event WHERE event_id = %s" % (event_id,)  # Fixing query format
    delete(query)  # Pass only one argument
    flash("Event deleted successfully!")
    return redirect(url_for('aasha_worker.aasha_worker_add_event'))



