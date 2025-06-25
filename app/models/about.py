from app import db 

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    year = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))