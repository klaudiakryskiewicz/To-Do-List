import calendar
from time import strptime

from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta, date
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

menu = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""

print(menu)
choice = int(input())


def day_task(day):
    rows = session.query(Table).filter(func.DATE(Table.deadline == day))
    print(day.strftime("%A"), day.day, day.strftime("%B") + ":")
    if rows.count() >0:
        for i, row in zip(range(rows.count()), rows):
            print(f"{i+1}.{row.task}")
    else:
        print("Nothing to do!")


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


while choice != 0:
    print("")
    #today's tasks
    if choice == 1:
        day_task(datetime.today().date())

    #week's tasks
    elif choice == 2:
        for day in daterange(datetime.today(), datetime.today() + timedelta(days=7)):
            day_task(day)
            print("")

    #all tasks
    elif choice == 3:
        rows = session.query(Table).order_by(Table.deadline)
        if rows.count() >0:
            for row in rows:
                print(f"{row.task}. {str(row.deadline.day)} {calendar.month_abbr[row.deadline.month]}")
        else:
            print("Nothing to do!")

    #missed tasks
    elif choice == 4:
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline)
        if rows.count() > 0:
            print("Missed tasks:")
            for row in rows:
                print(f"{row.task}. {str(row.deadline.day)} {calendar.month_abbr[row.deadline.month]}")
        else:
            print("Nothing is missed!")

    #add task
    elif choice == 5:
        task = input("Enter task\n")
        deadline = input("Enter deadline\n")
        new_row = Table(task=task)
        y, m, d = deadline.split('-')
        deadline = datetime(int(y), int(m), int(d))
        new_row.deadline = deadline
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    #delete task
    elif choice == 6:
        print("Choose the number of the task you want to delete")
        rows = session.query(Table).order_by(Table.deadline)
        if rows.count() > 0:
            for i, row in zip(range(rows.count()),rows):
                print(f"{i+1}. {row.task}. {str(row.deadline.day)} {calendar.month_abbr[row.deadline.month]}")
            task_number = int(input())
            session.delete(rows[task_number-1])
            session.commit()
            print("The task has been deleted!")
    print("")
    print(menu)
    choice = int(input())

if choice == 0:
    print("Bye!")
