from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import join
from sqlalchemy import and_,or_
from sqlalchemy.sql import select
import sqlite3

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# Creating model table for our CRUD database

###### Table Student ######
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Stuname = db.Column(db.String(100))
    Stuemail = db.Column(db.String(100))
    Stuphone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.Stuname = name
        self.Stuemail = email
        self.Stuphone = phone

###### Table Subject ######
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    teacher = db.Column(db.String(100))
    
    def __init__(self, subject, teacher):
        self.subject = subject
        self.teacher = teacher

###### Table join ######
class Join(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jname = db.Column(db.Integer,db.ForeignKey('student.id'))
    jsub = db.Column(db.Integer,db.ForeignKey('subject.id'))
   
    def __init__(self, jname, jsub):
        self.jname = jname
        self.jsub = jsub

#######index########
@app.route('/')
def Index():
    all_Student = Student.query.all()
    all_Subject = Subject.query.all()
    all_data = db.session.query(
        Join.id,Student.Stuname,Subject.subject,Subject.teacher
    ).outerjoin(Student,Join.jname==Student.id)\
    .outerjoin(Subject,Join.jsub==Subject.id )\
    .all()
    return render_template("index.html",students=all_Student ,Subject=all_Subject,alldata=all_data)


#######insert########
#table Student
@app.route('/insertstu', methods=['GET', 'POST'])
def insertstu():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_Student = Student(name, email, phone)
        db.session.add(my_Student)
        db.session.commit()

        flash("Student Inserted Successfully")
        return redirect(url_for('Index'))
    
    return render_template("insertStu.html")

#table Subject
@app.route('/insertsub', methods=['GET', 'POST'])
def insertsub():
    if request.method == 'POST':
        subject = request.form['subject']
        teacher = request.form['teacher']

        subject_data = Subject(subject,teacher)
        db.session.add(subject_data)
        db.session.commit()

        flash("Subject Inserted Successfully")
        return redirect(url_for('Index'))
    return render_template("insertSub.html")

#table join
@app.route('/insertjoin', methods=['GET', 'POST'])
def insertjoin():
    if request.method == 'POST':
        name = request.form['name']
        sub = request.form['sub']

        join_data = Join(name,sub)
        db.session.add(join_data)
        db.session.commit()

        flash(" Inserted Successfully")
        return redirect(url_for('Index'))
    all_Student = Student.query.all()
    all_Subject = Subject.query.all()
    return render_template("insert.html",students=all_Student,subjects=all_Subject)

#######Update########
#table student
@app.route('/updateStu/<id>', methods=['GET', 'POST'])
def updatestu(id):
    if request.method == 'POST':
        my_Student = Student.query.get(request.form.get('id'))
        my_Student.Stuname = request.form['name']
        my_Student.Stuemail = request.form['email']
        my_Student.Stuphone = request.form['phone']

        db.session.commit()
        flash("Student Updated Successfully")
        return redirect(url_for('Index'))

    my_Student = Student.query.get(id)
    return render_template('updateStu.html',student = my_Student)

#table subject
@app.route('/updateSub/<id>', methods=['GET', 'POST'])
def updatesub(id):
    if request.method == 'POST':
        my_Subject = Subject.query.get(request.form.get('id'))
        my_Subject.subject = request.form['subject']
        my_Subject.teacher = request.form['teacher']
        
        db.session.commit()
        flash("Subject Updated Successfully")
        return redirect(url_for('Index'))

    my_Subject = Subject.query.get(id)
    return render_template('updateSub.html',subject = my_Subject)

#table join
@app.route('/updateTable/<id>', methods=['GET', 'POST'])
def update_table_join(id):
    if request.method == 'POST':
        my_Table = Join.query.get(request.form.get('id'))
        my_Table.jname = request.form['name']
        my_Table.jsub = request.form['sub']

        db.session.commit()
        flash("Updated Successfully")
        return redirect(url_for('Index'))

    all_Student = Student.query.all()
    all_Subject = Subject.query.all()
    my_Table = Join.query.get(id)
    return render_template('updateTable.html',idTable = my_Table,students=all_Student,subjects=all_Subject)


#######delete########
#table Student
@app.route('/deleteStu/<id>/', methods=['GET', 'POST'])
def delete_stu(id):
    my_Student = Student.query.get(id)
    db.session.delete(my_Student)
    db.session.commit()
    flash("Student Deleted Successfully")
    return redirect(url_for('Index'))

#table Subject
@app.route('/deleteSub/<id>/', methods=['GET', 'POST'])
def delete_sub(id):
    my_Subject = Subject.query.get(id)
    db.session.delete(my_Subject)
    db.session.commit()
    flash("Subject Deleted Successfully")
    return redirect(url_for('Index'))

#table Join
@app.route('/deleteTable/<id>/', methods=['GET', 'POST'])
def delete_table_join(id):
    Join_table = Join.query.get(id)
    db.session.delete(Join_table)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for('Index'))

if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run(host='127.0.0.1', port=8080)


# การใช้ filter เพิ่มเติม
# Equals
# result = session.query(Customers).filter(Customers.id == 2)

# Not Equals
# result = session.query(Customers).filter(Customers.id! = 2)

# Like
# result = session.query(Customers).filter(Customers.name.like('Ra%'))

# IN
# result = session.query(Customers).filter(Customers.id.in_([1,3]))

# AND
# result = session.query(Customers).filter(and_(Customers.id>2, Customers.name.like('Ra%')))

# Or
# result = session.query(Customers).filter(or_(Customers.id>2, Customers.name.like('Ra%')))