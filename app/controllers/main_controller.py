from app import app
from flask import render_template
from flask_login import login_required


@app.route('/')
@login_required
def main():
    return render_template('main.html')