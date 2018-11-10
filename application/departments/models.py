from application import db

class Dept(db.Model):

    __tablename__ = "department"
  
    DepartmentID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(144), nullable=False)
    CreatedOn = db.Column(db.DateTime, default=db.func.current_timestamp())
    ModifiedOn = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    #Relationships
    accounts = db.relationship("User", backref='department', lazy=True)

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