from application import db
from application.models import Base, science2thesis
import os
from sqlalchemy.sql import text

class Science(Base):

    __tablename__ = "science"
  
    scienceID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    science2thesis = db.relationship("Thesis", secondary = science2thesis,
                               backref=db.backref('sciences', lazy = 'dynamic'))


    def __init__(self, name):
        self.name = name

    # Fetch data if science is linked with thesis to prevent deletion   
    if os.environ.get("HEROKU"):
    
        @staticmethod
        def sciWithThesis():
            stmt = text('SELECT science."scienceID", COUNT(science2thesis."thesisID") FROM science' 
                        ' LEFT JOIN science2thesis ON science."scienceID" = science2thesis."scienceID"'
                        ' WHERE science2thesis."thesisID" IS NOT NULL'
                        ' GROUP BY science."scienceID";')
            result = db.engine.execute(stmt)
            ids = []
            for row in result:
                ids.append({"id":row[0],"count":row[1]})
           
            return ids
   
    else:
    
        @staticmethod
        def sciWithThesis():
            stmt = text("SELECT science.scienceID, COUNT(science2thesis.thesisID) FROM science" 
                        " LEFT JOIN science2thesis ON science.scienceID = science2thesis.scienceID"
                        " WHERE science2thesis.thesisID IS NOT NULL"
                        " GROUP BY science.scienceID;")
            result = db.engine.execute(stmt)
            ids = []
            for row in result:
                print(row[0])
                ids.append({"id":row[0],"count":row[1]})
            
            return ids
    
        