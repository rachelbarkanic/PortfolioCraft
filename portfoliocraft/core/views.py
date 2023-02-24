from portfoliocraft.models import Project
from flask import render_template, request, Blueprint

core = Blueprint('core', __name__)

@core.route('/')
def index():

    page = request.args.get('page', 1 , type=int)
    projects = Project.query.order_by(Project.date.desc()).paginate(page = page, per_page = 4)

    return render_template('index.html', projects = projects)

@core.route('/info')
def info():
    return render_template('info.html')