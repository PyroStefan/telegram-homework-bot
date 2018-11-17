import os
import sys
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.schema import Table

Base = declarative_base()




class Homework(Base):
    __tablename__ = 'homework'
    id = Column(Integer, primary_key=True)
    subject = Column(String(250), nullable=False)
    todo = Column(String(5000), nullable=False)
    date_added = Column(DateTime(timezone=False))



def db_maker():
    engine = create_engine(
        'sqlite:///../db/homework.db')  # create the engine
    Base.metadata.create_all(engine)  # creates table

    # inserts some automatic stuff
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    subjects = [
        "ANA-1A", 
        "lin.algebra", 
        "ETM1", 
        "EV1", 
        "vaktekenen", 
        "informatica", 
        "netwerken",
        ]

    for subject in subjects:
        homework = Homework(subject=subject, todo="nothing", date_added=datetime.now())
        session.add(homework)
        session.commit()



if __name__ == "__main__":
    db_maker()