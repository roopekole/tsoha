from application import db
from application.models import Base, science2thesis

class Science(Base):

    __tablename__ = "science"
  
    scienceID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    science2thesis = db.relationship("Thesis", secondary = science2thesis,
                               backref=db.backref('sciences', lazy = 'dynamic'))


    def __init__(self, name):
        self.name = name
        