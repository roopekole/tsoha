from application import db
from application.models import Base

class Dept(Base):

    __tablename__ = "department"
  
    departmentID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    

    #Relationships
    accounts = db.relationship("User", backref='user_department', lazy=True)

    def __init__(self, name):
        self.name = name
        