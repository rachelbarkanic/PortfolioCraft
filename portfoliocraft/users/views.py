from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from portfoliocraft import db
from portfoliocraft.models import User, Project
from portfoliocraft.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from portfoliocraft.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can log in!')
        return redirect(url_for('users.login'))

    return render_template('register.html', form = form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.validate_password(form.password.data) and user is not None:
            login_user(user)
            flash('You are logged in!')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
        elif user is None: 
            flash('Invalid login!')
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
    
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
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
    user = User.query.filter_by(username = username).first_or_404

    projects = Project.query.filter_by(author = user).order_by(Project.date.desc()).paginate(page = page, per_page = 5)
    # might have issues here

    return render_template('user_projects.html', projects = projects, user = user)