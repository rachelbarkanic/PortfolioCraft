from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from portfoliocraft import db
from portfoliocraft.models import Project
from portfoliocraft.projects.forms import ProjectForm
from portfoliocraft.projects.screenshot_handler import screenshot_upload

projects = Blueprint('projects', __name__)


@projects.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():


        project = Project(title = form.title.data,
                    description = form.description.data,
                    demo_link = form.demo_link.data,
                    github_link = form.github_link.data,
                    user_id = current_user.id)

        db.session.add(project)
        db.session.commit()

        if form.screenshot.data:
            screenshot = project.id
            pic = screenshot_upload(form.screenshot.data, screenshot)
            project.screenshot = pic
        
        db.session.commit()


        return redirect(url_for('core.index'))
    
    return render_template('create_project.html', form = form)


@projects.route('/<int:project_id>')
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', title=project.title, date = project.date, project = project, screenshot = project.screenshot)



@projects.route('/<int:project_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):

    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        abort(403)
    
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('core.index'))
