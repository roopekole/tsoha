from application import db
from application.models import Base, science2thesis

class Thesis(Base):
    thesisID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    level = db.Column(db.Boolean)
    author = db.Column(db.String(144), nullable=True)
    status = db.Column(db.Integer)
    completedOn = db.Column(db.DateTime)
    reservedOn = db.Column(db.DateTime, nullable = True)

    userID = db.Column(db.String, db.ForeignKey('account.userID'),
                           nullable=False)
    

    #Relationships
    science2thesis = db.relationship("Science", secondary = science2thesis,
                               backref=db.backref('theses', lazy = 'joined'))
    

    def __init__(self, title, description, user):
        self.title = title
        self.description = description
        self.status = 0
        self.userID = user
