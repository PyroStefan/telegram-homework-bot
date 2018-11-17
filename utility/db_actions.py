from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utility.db_init import Homework, Base

from datetime import date, datetime

def query_homework_by_subject(subject, session):
    '''Queries database for rows which contain homework of this subject. Returns a list of Homework objects.'''
    subject_homework = session.query(Homework).filter(Homework.subject == subject).all()
    return subject_homework


def query_all_homework(session):
    '''Queries database for all rows, returns a list of Homework objects.'''
    all = session.query(Homework).all()
    return all


def add_hw(subject, todo, session):
    """Adds a new homework entry to the database."""
    new_entry = Homework(subject=subject,
    todo=todo,
    date_added=date.today())
    session.add(new_entry)
    session.commit()


def del_hw(id, session):
    """Deletes row with matching id."""
    entry = session.query(Homework).filter(Homework.id == id).first()
    session.delete(entry)
    session.commit()
    



# if __name__ == "__main__":

#     engine = create_engine('sqlite:///../db/homework.db')
#     Base.metadata.bind = engine
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     # add_hw("nonsense", "som inf", session)
#     a = query_all_homework(session)

#     for hw in a:
#         print(hw.id, hw.subject, hw.todo, hw.date_added)

#     b = query_homework_by_subject("ANA-1A", session)

#     for hw in b:
#         print(hw.id, hw.subject, hw.todo, hw.date_added)

    
