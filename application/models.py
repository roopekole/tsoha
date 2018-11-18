from application import db

class Base(db.Model):

    __abstract__ = True
    createdOn = db.Column(db.DateTime, default=db.func.current_timestamp())
    modifiedOn = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


science2thesis = db.Table('science2thesis', 
                          db.Column('thesisID', db.Integer, db.ForeignKey('thesis.thesisID')),
                          db.Column('scienceID', db.Integer, db.ForeignKey('science.scienceID')))