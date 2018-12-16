from application import db
from application.models import Base
from sqlalchemy.sql import text
import os
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

    # Using different aggregate statements to deal with postgresqls double quotatation properties
    # Note to self, do not use upper case in model attributes when dealing with postgres
    # Alternatively the tables in postgres need to be created without quotation to force lowercase

    if os.environ.get("HEROKU"):
        @staticmethod
        def countInactives():
            stmt = text("SELECT COUNT('userID') FROM account WHERE inactive")
            result = db.engine.execute(stmt)
            for row in result:
                count = row[0]
            return count
    
        @staticmethod
        def countTheses():
            stmt = text("SELECT account.'userID', COUNT(thesis.'thesisID')"
                        " FROM account LEFT JOIN thesis ON thesis.'userID' = account.'userID'"
                        " WHERE account.admin = 0" 
                        " GROUP BY account.'userID';")
            result = db.engine.execute(stmt)
            count = []
            for row in result:
                print(row[1])
                count.append({"id":row[0], "count":row[1]})

            return count
   
    else:
        @staticmethod
        def countInactives():
            stmt = text("SELECT COUNT(userID) FROM account WHERE inactive")
            result = db.engine.execute(stmt)
            for row in result:
                count = row[0]
            return count
    
        @staticmethod
        def countTheses():
            stmt = text("SELECT account.userID, COUNT(thesis.thesisID)"
                        " FROM account LEFT JOIN thesis ON thesis.userID = account.userID"
                        " WHERE account.admin = 0" 
                        " GROUP BY account.userID;")
            result = db.engine.execute(stmt)
            count = []
            for row in result:
                print(row[1])
                count.append({"id":row[0], "count":row[1]})

            return count
    