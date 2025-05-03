from flask import *

from public import public
from werkzeug.security import generate_password_hash

from admin import admin
from hospital import hospital
from doctor import doctor
from pharmacy import pharmacy
from aasha_worker import aasha_worker
from user import user
from lab import lab
from flask_mail import Mail, Message
import random
from database import *

app=Flask(__name__)
app.secret_key='alex'

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(hospital,url_prefix='/hospital')
app.register_blueprint(doctor,url_prefix='/doctor')
app.register_blueprint(pharmacy,url_prefix='/pharmacy')
app.register_blueprint(aasha_worker,url_prefix='/aasha_worker')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(lab,url_prefix='/lab')
# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'annaeldho4@gmail.com'
app.config['MAIL_PASSWORD'] = 'fvhj ykzo epra turg'
mail = Mail(app)

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST' and 'submitbutton' in request.form:
      uname = request.form.get('uname')
      email = request.form.get('email')  # Use request.form instead of request.json

      vv = "SELECT * FROM patients INNER JOIN login USING(login_id) WHERE username='%s' AND email='%s'" % (uname, email)
      cc = select(vv)

      if cc:
          otp = random.randint(100000, 999999)
          session['otp'] = otp  # Store OTP in session
          session['uname'] = uname  # Store OTP in session

          msg = Message('Your OTP Code', sender='annaeldho4@gmail.com', recipients=[email])
          msg.body = f'Your OTP code is {otp}. Do not share it with anyone.'
          mail.send(msg)

          flash("OTP sent successfully!")  # You can redirect to OTP verification page
          return redirect(url_for('verify_otp_and_chage_password'))
      else:
          flash("Invalid username or email..........!")  # You can redirect to OTP verification page
          return redirect(url_for('forget_password'))    
    return render_template('forget_password.html')


@app.route('/verify_otp_and_chage_password', methods=['GET', 'POST'])
def verify_otp_and_chage_password():
    if request.method == 'POST' and 'submitbutton' in request.form:
        otp = request.form.get('otp')
        new_password = request.form.get('new_password')
        hashed_pwd = generate_password_hash(new_password)

        # Ensure OTP exists in session before checking
        if 'otp' in session and int(otp) == int(session['otp']):
            # Update password (assuming 'login_id' is linked to the user)
            nn="SELECT login_id FROM login WHERE username='%s'"%(session['uname'])
            qq=select(nn)
            cc = "UPDATE login SET password='%s' WHERE login_id = '%s'" % (hashed_pwd,qq[0]['login_id'] )
            update(cc)

            # Clear OTP session after successful verification
            session.pop('otp', None)
            session.pop('uname', None)

            flash("Password updated successfully!")
            return redirect(url_for('public.login'))  # Ensure public.login exists as a valid route
        else:
            flash("Invalid OTP! Please try again.")

    return render_template('verify_otp_and_chage_password.html')
  
if __name__ == '__main__':
    app.run(debug=True, port=6166)