from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()




print("""1) Today's tasks
2) Add task
0) Exit""")
choice = int(input())

while choice != 0:
    if choice == 1:
        rows = session.query(Table).filter(Table.deadline==datetime.today())
        for row in rows:
            print(row.task)
        else:
            print("Nothing to do!")

    elif choice == 2:
        task = input("Enter task\n")
        new_row = Table(task=task)
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    print("""1) Today's tasks
    2) Add task
    0) Exit""")
    choice = int(input())

if choice == 0:
    print("Bye!")