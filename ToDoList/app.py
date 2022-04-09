from turtle import pos
from forms import RegisterForm, LoginForm
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import date
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

Bootstrap(app)

app.config['SECRET_KEY'] = 'y39Oenedfd845613fsdgs8d4g513s8afg46a5f32gza8hjn'

login_manager = LoginManager(app)

# Create databases for tasks and users

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    lists = db.relationship('List', backref='user', lazy=True)
    
class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tasks = db.relationship('Task', backref='list', lazy=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
        
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=False, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    
# db.create_all()
    
# This is to temporarily hold tasks Until they are saved to the database or till connection the server is ended
global tasks
tasks = []

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# This is to save the list
@app.route('/save', methods=['POST', 'GET'])
def save():
    if current_user.is_authenticated:
        new_list = List(user_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()
        current_list = List.query.filter_by(user_id=current_user.id).order_by(List.id.desc()).first()
        for task in tasks: # Loops through the task list and gets the key value pair in each dictionary
            for key, value in task.items():
                new_task = Task(task=key, list_id=current_list.id, completed=value)
                db.session.add(new_task)
        db.session.commit()
        tasks.clear()
        return redirect(url_for('new'))
    else:
        flash("You need to sign in to be able to save a list")
        return redirect(url_for('login'))


@app.route("/new", methods=["GET", "POST"]) # Page to type in your tasks
def new():
    today = date.today().strftime("%d/%m/%Y")
    if current_user.is_authenticated:
        lists = List.query.filter_by(user_id=current_user.id).all()
        if request.method == "GET":
            amount = len(tasks)
            return render_template('task.html', tasks=tasks, date=today,
            amount=amount, user=current_user, lists=lists, from_list=True, save=False, update=False)
        if request.method == "POST": # This adds the task to the list and gives it a completed value of zero
            tasks.append(
                {request.form.get('task'):False}
                )
            amount = len(tasks)
            return render_template('task.html', tasks=tasks, date=today,
            amount=amount, user=current_user, lists=lists, from_list=True, save=False)
    else:
        if request.method == "GET":
            amount = len(tasks)
            return render_template('task.html', tasks=tasks, date=today,
            amount=amount, user=current_user, from_list=True, save=False, update=False)
        if request.method == "POST":  # This adds the task to the list and gives it a completed value of zero
            tasks.append(
                {request.form.get('task'):False}
                )
            amount = len(tasks)
            return render_template('task.html', tasks=tasks, date=today,
            amount=amount, user=current_user, from_list=True, save=False, update=False)

@app.route("/login", methods=["POST", "GET"]) # Login page
def login():
    if current_user.is_authenticated:
        logout_user()
        flash('Logged out successfully! ')
        return redirect(url_for('login'))
    else:    
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=True)
                    return redirect(url_for('new'))
                else:
                    flash('Incorrect email or password')
                    return redirect(url_for('login'))
            else:
                flash('Looks like you have not yet registered')
                return redirect(url_for('register'))
        else:        
            return render_template('login.html', form=form, reg=False)


@app.route("/register", methods=["POST", "GET"]) # Registeration page
def register():
    form = RegisterForm()
    if form.validate_on_submit(): # Adds the user to the database on submission of the registeration form
        first_name = form.firstname.data
        last_name = form.lastname.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='pbkdf2:sha256',
                                          salt_length=9)
        # Check if the user is already in the database
        user = User.query.filter_by(email=email).first() 
        if user:
            flash('Looks like you have already registered. Login instead')
            return redirect(url_for('login'))
        else:
            new_user = User(email=email, firstname=first_name, lastname=last_name,
                    password=password)
        
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)
            return redirect(url_for('new'))
    return render_template('login.html', form=form, reg=True)
 
 
# This is to view individual lists and their items    
@app.route('/<path:item>/<path:date>', methods=["POST", "GET"])
def item(item, date):
    if request.method == "GET":
        lists = List.query.filter_by(user_id=current_user.id).all()
        list = List.query.filter_by(id=item, user_id=current_user.id).first()
        date = list.date.strftime("%d/%m/%Y")
        tasks = Task.query.filter_by(list_id=list.id).all()
        amount = len(tasks)
        return render_template('task.html', tasks=tasks, date=date, list=list,
         amount=amount, user=current_user, lists=lists, from_list=False, save=True, update=False, previous=True)
    if request.method == "POST":
        lists = List.query.filter_by(user_id=current_user.id).all()
        list = List.query.filter_by(id=item, user_id=current_user.id).first()
        date = list.date.strftime("%d/%m/%Y")
        new_task = Task(task=request.form.get('task'), completed=False, list_id=list.id)
        db.session.add(new_task)
        db.session.commit()
        tasks = Task.query.filter_by(list_id=list.id).all()
        amount = len(tasks)
        return render_template('task.html', tasks=tasks, date=date,
                amount=amount, user=current_user, lists=lists, from_list=False, save=False)
                
        
# This checks a task from the database as completed
@app.route('/completed/<int:id>')
def completed(id):
    task = Task.query.filter_by(id=id).first()
    task.completed = True
    db.session.commit()
    list = List.query.filter_by(id=task.list_id).first()
    return redirect(url_for('item', item=list.id, date=list.date))


# Convert name from string to dictionary
# This is for when the task has not been saved to the database
def convert(name):
    remove = "{}' "
    for char in remove:
        name = name.replace(char, "")
    name = name.split(':')
    if name[1] == 'False':
        return {name[0]:False}
    else:
        return {name[0]:True}


# This checks a task from the list as completed
@app.route('/comp_list/<path:name>')
def comp_list(name):
    name = convert(name=name)
    # Compare with task in tasks
    for task in tasks:
        for key in name.keys():
            if key in task.keys():
                task[key] = True
                print(task)            
    return redirect(url_for('new'))

# This updates a task and therefore a list
# This updates a task from the database
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if request.method == "GET":
        task = Task.query.filter_by(id=id).first()
        list = List.query.filter_by(id=task.list_id, user_id=current_user.id).first()
        lists = List.query.filter_by(user_id=current_user.id).all()
        date = list.date.strftime("%d/%m/%Y")
        tasks = Task.query.filter_by(list_id=list.id).all()
        amount = len(tasks)
        return render_template('task.html', tasks=tasks, date=date,
         amount=amount, user=current_user, lists=lists, from_list=False, save=True, update=True, task=task)
    if request.method == "POST":
        task = Task.query.filter_by(id=id).first()
        list = List.query.filter_by(id=task.list_id, user_id=current_user.id).first()
        task.task = request.form.get('task')
        db.session.commit()
        return redirect (url_for('item', item=list.id, date=list.date))
    
    
# This is to update a task from the python list
@app.route("/upd_list/<path:name>", methods=["GET", "POST"])
def upd_list(name):
    today = date.today().strftime("%d/%m/%Y")
    if request.method == "GET":
        for task in tasks:
            for key, value in task.items():
                if key == name:
                    global pos
                    pos = tasks.index(task)
                    global item
                    item = key
        amount = len(tasks)
        return render_template('task.html', tasks=tasks, date=today,
        amount=amount, user=current_user, from_list=True, save=False, update=True, task=item)
        # Compare with task in tasks
    if request.method == "POST":
        new = request.form.get('task')
        tasks[pos] = {new: tasks[pos][item]}
        return redirect(url_for('new'))
        
        
# This deletes a list
# This deletes a task from the database
@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.filter_by(id=id).first()
    list = List.query.filter_by(id=task.list_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('item', item=list.id, date=list.date))

# This deletes a task from the python list
@app.route('/del_list/<path:name>')
def del_list(name):
    name = convert(name=name)
    # Compare with task in tasks
    for task in tasks:
        for key in name.keys():
            if key in task.keys():
                tasks.remove(task)        
    return redirect(url_for('new'))


if __name__ == "__main__":
    app.run(debug=True)