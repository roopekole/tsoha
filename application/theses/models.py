from application import db

class Thesis(db.Model):
    ThesisID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(144), nullable=False)
    Description = db.Column(db.String(144), nullable=False)
    Level = db.Column(db.Boolean)
    Author = db.Column(db.String(144), nullable=True)
    Status = db.Column(db.Integer)
    CreatedOn = db.Column(db.DateTime, default=db.func.current_timestamp())
    CompletedOn = db.Column(db.DateTime, default=db.func.current_timestamp())
    ReservedOn = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    UserID = db.Column(db.String, db.ForeignKey('account.UserID'),
                           nullable=False)



    def __init__(self, title, description, user):
        self.Title = title
        self.Description = description
        self.Status = 0
        self.UserID = user