from application import db

class User(db.Model):

    __tablename__ = "account"
  
    UserID = db.Column(db.String(100), primary_key=True)
    FirstName = db.Column(db.String(144), nullable=False)
    LastName = db.Column(db.String(144), nullable=False)
    Password = db.Column(db.String(144), nullable=False)
    Admin = db.Column(db.Integer)
    Department = db.Column(db.Integer, db.ForeignKey('department.DepartmentID'),
                           nullable=True)
    CreatedOn = db.Column(db.DateTime, default=db.func.current_timestamp())
    ModifiedOn = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    #Relationships
    theses = db.relationship("Thesis", backref='account', lazy=True)

    def __init__(self, userid, firstname, lastname, password, admin):
        self.UserID = userid
        self.FirstName = firstname
        self.LastName = lastname
        self.Password = password
        self.Admin = 1
  
    def get_id(self):
        return self.UserID

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True