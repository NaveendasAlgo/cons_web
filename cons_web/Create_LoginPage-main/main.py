########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, flash,request,redirect,url_for,Response
from flask_login import login_required, current_user
from __init__ import create_app, db
from sqlalchemy.inspection import inspect
from models import Data
import pandas as pd
from collections import defaultdict

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    if current_user.ishead:
        return render_template('profile_admin.html', name=current_user.name)
    else:
        return render_template('profile.html', name=current_user.name)



def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

@main.route('/insert' , methods=['GET', 'POST']) # profile page that return 'profile'
@login_required
def insert():  
    if request.method=='GET': # If the request is GET we return the sign up page and forms
        return render_template('insert.html', name=current_user.name)
    else: # if the request is POST, then we check if the email doesn't already exist and then we save data
        state = request.form.get('country-state')
        district=request.form.get('District')
        sub_district=request.form.get('Sub-District')
        panchayat=request.form.get('Panchayat')
        no_audit=request.form.get('Number_of_audits')
        name=current_user.name
        new_data = Data(state=state, district=district, sub_district=sub_district,panchayat=panchayat,no_audit=no_audit,name=name) #
        # add the new user to the database
        db.session.add(new_data)
        db.session.commit()
        result=Data.query.all()
        df = pd.DataFrame(query_to_dict(result))
        # df.to_excel("TEST1.xlsx",index=False)
        flash("record inserted successfully!","success")
        return redirect(url_for('main.insert'))

@main.route('/dnld' , methods=['GET', 'POST']) # profile page that return 'profile'
@login_required
def dnld():
    if current_user.ishead:
        result=Data.query.all()
        df = pd.DataFrame(query_to_dict(result))
        return Response(df.to_csv(), mimetype="text/csv",headers={"Content-disposition": "attachment; filename=merged_file.csv"})
        # df.to_excel("TEST1.xlsx",index=False)


        
        



        # name = request.form.get('name')
        # password = request.form.get('password')
        # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        # if user: # if a user is found, we want to redirect back to signup page so user can try again
        #     flash('Email address already exists')
        #     return redirect(url_for('auth.signup'))
        # # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256')) #
        # # add the new user to the database
        # db.session.add(new_user)
        # db.session.commit()
        # return redirect(url_for('auth.login'))
app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode