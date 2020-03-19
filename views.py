from .database import db
from .app import app
from flask import Flask, render_template, request, redirect
from .models import User, Login

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        login = Login(uname=request.form['username'], password=request.form['pass'])

        try:
            db.session.add(login)
            db.session.commit()

            db.session.refresh(login)
            print(login.id)

            user  = User(login_id=login.id, name=request.form['name'], address=request.form['address'], number=request.form['number'])
            db.session.add(user)
            db.session.commit()

            return redirect('/viewall')
        except:
            return 'Error'
    else:
        return render_template('index.html')

@app.route('/viewall')
def viewAll():
    user = User.query.order_by(User.name).all()

    return render_template('viewall.html', users=user)

@app.route('/delete/<int:id>')
def delete(id):
    # 404 means NOT FOUND
    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        # session.delete() <---- is equivalent to DELETE FROM in mysql
        db.session.commit()
        # commit means execute/run/go

        return redirect('/viewall')
    except:
        return 'Error in deleting user'
