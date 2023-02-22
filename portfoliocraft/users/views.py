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
        return redirect(url_for('login'))

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
    return render_template('login.html', form = form)



@users.route('/logout')
def logout():
    '''log user out '''
    logout_user()
    return redirect(url_for('core.index'))