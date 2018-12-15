from application import db
from application.models import Base
from sqlalchemy.sql import text
class User(Base):

    __tablename__ = "account"
  
    userID = db.Column(db.String(100), primary_key=True, nullable=False)
    firstName = db.Column(db.String(144), nullable=False)
    lastName = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    admin = db.Column(db.Integer) # Kept as integer for future admin role types
    inactive = db.Column(db.Boolean)
    department = db.Column(db.Integer, db.ForeignKey('department.departmentID'),
                           nullable=True)
    

    #Relationships
    theses = db.relationship("Thesis", backref='account', lazy=True)

    def __init__(self, userid, firstname, lastname, password, department, admin):
        self.userID = userid
        self.firstName = firstname
        self.lastName = lastname
        self.password = password
        self.department = department
        self.admin = admin
  
    def get_id(self):
        return self.userID

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        return ["ADMIN"]

    @staticmethod
    def countInactives():
        stmt = text("SELECT COUNT('userID') FROM account WHERE inactive LIMIT 1")
        result = db.engine.execute(stmt)
        for row in result:
            count = row[0]
        return count
    
    # does not work locally

    @staticmethod
    def countTheses():
        stmt = text("SELECT 'account.userID' as user, COUNT('thesis.thesisID')"
                    " FROM account LEFT JOIN thesis ON 'thesis.userID' = 'account.userID'"
                    " WHERE account.admin = 0" 
                    " GROUP BY user;")
        result = db.engine.execute(stmt)
        count = []
        for row in result:
            count.append({"id":row[0], "count":row[1]})

        return count
   