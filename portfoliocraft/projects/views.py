from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from portfoliocraft import db
from portfoliocraft.models import Project
from portfoliocraft.projects.forms import ProjectForm

projects = Blueprint('projects', __name__)

#CREATE
@projects.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():

        project = Project(title = form.title.data,
                    description = form.description.data,
                    screenshot = form.screenshot.data,
                    demo_link = form.demo_link.data,
                    github_link = form.github_link.data,
                    user_id = current_user.id,
                    )
        db.session.add(project)
        db.session.commit()
        flash('Project Added!!')
        return redirect(url_for('core.index'))
    
    return render_template('create_project.html', form = form)

#READ
@projects.route('/<int:project_id>')
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', title=project.title, date = project.date, project = project)


#UPDATE
@projects.route('/<int:project_id>/update', methods=['GET', 'POST'])
@login_required
def update(project_id):
    project = Project.query.get_or_404(project_id)

    if project.author != current_user:
        abort(403)
    
    form = ProjectForm()

    if form.validate_on_submit():

        project.title = form.title.data,
        project.description = form.description.data,
        project.screenshot = form.screenshot.data,
        project.demo_link = form.demo_link.data,
        project.github_link = form.github_link.data

        db.session.commit()
        flash('Project Updated!')
        return redirect(url_for('project.project', project_id = project.id))
    
    elif request.method == 'GET':
         form.title.data = project.title
         form.description.data = project.description
         form.screenshot.data = project.screenshot
         form.demo_link.data = project.demo_link
         form.github_link.data = project.github_link

    return render_template('create_project.html', title = 'Updating', form = form)

#DELETE
@projects.route('/<int:project_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):

    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        abort(403)
    
    db.session.delete(project)
    db.session.commit()
    flash('Project Deleted!')
    return redirect(url_for('core.index'))