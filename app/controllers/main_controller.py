from app import app
from flask import render_template
from flask_login import login_required
from app.models.about import Milestone

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/about')
def about():
    milestones = Milestone.query.order_by(Milestone.year.asc()).all()
    return render_template('main_screen/about.html', milestones=milestones)