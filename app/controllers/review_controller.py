from app import db
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_required
from app.models.product import Product
from app.models.review import Review
from app.forms.review_form import UserReviewForm


review_bp = Blueprint('review', __name__)

# @review_bp.route('/')