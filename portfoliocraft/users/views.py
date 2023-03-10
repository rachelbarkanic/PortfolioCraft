import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, session, send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from portfoliocraft import db, app, upload_folder
from portfoliocraft.models import User, Project
from portfoliocraft.users.forms import RegistrationForm, LoginForm, UpdateUserForm, ResumeForm
from portfoliocraft.users.picture_handler import add_profile_pic



users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    
    if form.validate_on_submit():
        existing_email = User.query.filter_by(email=form.email.data).first()
        existing_username = User.query.filter_by(username=form.username.data).first()
        
        if existing_username:
            flash('that username already exists, try another')
            return render_template('register.html', form = form)
        elif existing_email:
            flash('that email already exists, try another')
            return render_template('register.html', form = form)

        else:
            user = User(first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering. Please log in!')
            return redirect(url_for('users.login'))

    return render_template('register.html', form = form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.validate_password(form.password.data):
            login_user(user)
            flash('You are logged in!')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

        else:
            flash('Invalid email or password, please try again!')
            return redirect(url_for('users.login'))

    return render_template('login.html', form = form)



@users.route('/logout')
def logout():
    '''log user out '''
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():


    form = UpdateUserForm()
    
    if request.method == 'POST':

        form.validate_on_submit()

        user = User.query.filter_by(username = current_user.username).first()

        if form.picture.data:
            username = user.username
            pic = add_profile_pic(form.picture.data, username)
            user.profile_image = pic

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.username = form.username.data
        user.email = form.email.data

        db.session.commit()
        flash('Your Account Information Has Been Updated!')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image = profile_image, form = form)



@users.route('/<username>')
def user_projects(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username = username).first_or_404()

    projects = Project.query.filter_by(author = user).order_by(Project.date.desc()).paginate(page = page, per_page = 5)

    return render_template('user_projects.html', projects = projects, user = user)





@users.route('/resume', methods=['GET', 'POST'])
@login_required
def upload_file():

    user = User.query.filter_by(username = current_user.username).first()

    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        img = filename

        user.resume = img
        db.session.commit()

        return render_template('resume.html', img=img)
        
    return render_template('resume.html')


@users.route('/resume/<int:user_id>')
def view_resume(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('user_resume.html', user=user, title=user.username, resume = user.resume)

