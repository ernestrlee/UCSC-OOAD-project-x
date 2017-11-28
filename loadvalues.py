# This file loads data into the database "personaltrainer.db"
# SQL Alchemy is a Python SQL toolkit
# Imports / Configuration for sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import the classes used in the original database setup
from database_setup import Base, User, Trainee, Trainer, Exercise, Set, Routine, Routinelist

engine = create_engine('sqlite:///personaltrainer.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Add people to the system, user table
user1 = User(name="Pete Simons",
                 email="pete.simons@gg.net",
                 password="123",
                 birthdate="03/01/1980",
                 image="https://i.redd.it/fnf14eb7thsz.gif")

session.add(user1)
session.commit()

user2 = User(name="Jessica Peterson",
                 email="j.peterson@ff.net",
                 password="123",
                 birthdate="03/01/1990",
                 image="https://static.comicvine.com/uploads/square_small/11/114183/5147887-margesimpson.png")

session.add(user2)
session.commit()

user3 = User(name="John Smith",
                 email="j.smith@aa.net",
                 password="123",
                 birthdate="01/01/2000",
                 image="https://vignette.wikia.nocookie.net/simpsons/images/6/6d/Abraham_Simpson_I.png/revision/latest?cb=20130913052937")

session.add(user3)
session.commit()

user4 = User(name="Sarah Parker",
                 email="s.parker@ee.net",
                 password="123",
                 birthdate="10/01/1992",
                 image="https://vignette.wikia.nocookie.net/simpsons/images/6/6c/MaggieSimpson.PNG/revision/latest?cb=20170101014602")

session.add(user4)
session.commit()

user5 = User(name="Samuel Adams",
                 email="s.adams@cc.net",
                 password="123",
                 birthdate="12/13/2002",
                 image="http://vignette3.wikia.nocookie.net/simpsons/images/6/6b/600px-Sven_Simpson.png/revision/latest?cb=20120614000244")

session.add(user5)
session.commit()

user6 = User(name="Betsy Ross",
                 email="b.ross@dd.net",
                 password="123",
                 birthdate="04/13/1995",
                 image="https://upload.wikimedia.org/wikipedia/en/e/ec/Lisa_Simpson.png")

session.add(user6)
session.commit()


# Add trainer information to the trainer table
trainer1 = Trainer(years_experience="5",
                   gym="Gold's Gym",
                   education="Associates Degree Physical Education",
                   specialization="Strength training and mass building",
                   background="I've been a trainer for five years and have helped trained more than 300 people to reach their goals.",
                   user=user1)

session.add(trainer1)
session.commit()

trainer2 = Trainer(years_experience="12",
                   gym="24 hour fitness",
                   education="BS Kinesiology",
                   specialization="endurance, health",
                   background="I've been a trainer for twelve years and have helped trained more than 1000 people to reach their goals.",
                   user=user2)

session.add(trainer2)
session.commit()


# Add trainee information to the trainee table
trainee3 = Trainee(goal="build mass",
                   user=user3,
                   trainer=trainer1)

session.add(trainee3)
session.commit()

trainee4 = Trainee(goal="endurance",
                   user=user4,
                   trainer=trainer2)

session.add(trainee4)
session.commit()

trainee5 = Trainee(goal="body definition",
                   user=user5,
                   trainer=trainer1)

session.add(trainee5)
session.commit()

trainee6 = Trainee(goal="strength",
                   user=user6,
                   trainer=trainer1)

session.add(trainee6)
session.commit()


# Add exercises to exercise table
exercise1 = Exercise(name="Push-ups",
                     description="An exercise where a person lies down on the floor face down and pushes up with thier arms.",
                     imageurl="/static/images/pushups.png",
                     videourl="https://www.youtube.com/watch?v=Eh00_rniF8E",
                     body_parts="Pectorials, shoulders, and triceps",
                     type="Strength, endurance, body definition",
                     trainer=trainer1)

session.add(exercise1)
session.commit()

exercise2 = Exercise(name="Sit-ups",
                     description="An exercise where a person lies down on the floor on their back with thier knees bent and tries to sit up.",
                     imageurl="/static/images/situps.png",
                     videourl="https://www.youtube.com/watch?v=jDwoBqPH0jk",
                     body_parts="Abdominals",
                     type="Strength, endurance, body definition",
                     trainer=trainer1)

session.add(exercise2)
session.commit()

exercise3 = Exercise(name="Chin-ups",
                     description="An exercise where a person hangs onto a bar and tries to pull themselves up.",
                     imageurl="/static/images/chinups.png",
                     videourl="https://www.youtube.com/watch?v=_71FpEaq-fQ",
                     body_parts="Shoulders, upper back, biceps",
                     type="Strength, endurance, body definition",
                     trainer=trainer2)

session.add(exercise3)
session.commit()


exercise4 = Exercise(name="Jumping Jacks",
                     description="An exercise where a person jumps up and down while swinging their arms and legs in an out sideways.",
                     imageurl="/static/images/jumpingjacks.jpg",
                     videourl="https://www.youtube.com/watch?v=UpH7rm0cYbM",
                     body_parts="All",
                     type="Endurance, warmup",
                     trainer=trainer2)

session.add(exercise4)
session.commit()


exercise5 = Exercise(name="Squats",
                     description="An exercise where a person bends down with thier knees and stands back up.",
                     imageurl="/static/images/squats.jpg",
                     videourl="https://www.youtube.com/watch?v=nEQQle9-0NA",
                     body_parts="Legs",
                     type="Endurance, strength",
                     trainer=trainer2)

session.add(exercise5)
session.commit()

exercise6 = Exercise(name="Shoulder press",
                     description="An exercise where a person pushes weights from shoulder height to above their heads and lowers it back down to shoulder height.",
                     imageurl="/static/images/shoulderpress.png",
                     videourl="",
                     body_parts="Shoulders, triceps",
                     type="Endurance, strength",
                     trainer=trainer1)

session.add(exercise6)
session.commit()


# Add a routine to the routine table
routine1 = Routine(name="Super mega push ups",
                   description="Nothing but push ups.  Perform each set with 2 minutes of rest in between.",
                   difficulty="Hard",
                   trainer=trainer1)

session.add(routine1)
session.commit()

# Add sets to routine 1
set1 = Set(order="1",
           repetitions="20",
           exercise=exercise1,
           routine=routine1)

session.add(set1)
session.commit()

set2 = Set(order="2",
           repetitions="30",
           exercise=exercise1,
           routine=routine1)

session.add(set2)
session.commit()

set3 = Set(order="3",
           repetitions="40",
           exercise=exercise1,
           routine=routine1)

session.add(set3)
session.commit()

set4 = Set(order="4",
           repetitions="20",
           exercise=exercise1,
           routine=routine1)

session.add(set4)
session.commit()

set5 = Set(order="5",
           repetitions="10",
           exercise=exercise1,
           routine=routine1)

session.add(set5)
session.commit()


# Add a routine to the routine table
routine2 = Routine(name="Round about",
                   description="This routine goes through 5 different exercises.",
                   difficulty="Intermediate",
                   trainer=trainer1)

session.add(routine2)
session.commit()

# Add sets to routine 2
set1 = Set(order="1",
           repetitions="20",
           exercise=exercise1,
           routine=routine2)

session.add(set1)
session.commit()

set2 = Set(order="2",
           repetitions="30",
           exercise=exercise2,
           routine=routine2)

session.add(set2)
session.commit()

set3 = Set(order="3",
           repetitions="10",
           exercise=exercise3,
           routine=routine2)

session.add(set3)
session.commit()

set4 = Set(order="4",
           repetitions="20",
           exercise=exercise4,
           routine=routine2)

session.add(set4)
session.commit()

set5 = Set(order="5",
           repetitions="10",
           exercise=exercise5,
           routine=routine2)

session.add(set5)
session.commit()


# Add a routine to the routine table
routine3 = Routine(name="Round the clock",
                   description="This routine goes through 5 different exercises.",
                   difficulty="Intermediate",
                   trainer=trainer2)

session.add(routine3)
session.commit()

# Add sets to routine 3
set1 = Set(order="1",
           repetitions="20",
           exercise=exercise1,
           routine=routine3)

session.add(set1)
session.commit()

set2 = Set(order="2",
           repetitions="10",
           exercise=exercise5,
           routine=routine3)

session.add(set2)
session.commit()

set3 = Set(order="3",
           repetitions="5",
           exercise=exercise3,
           routine=routine3)

session.add(set3)
session.commit()

set4 = Set(order="4",
           repetitions="20",
           exercise=exercise4,
           routine=routine3)

session.add(set4)
session.commit()

set5 = Set(order="5",
           repetitions="10",
           exercise=exercise5,
           routine=routine3)

session.add(set5)
session.commit()

# Assign routines to trainees
routinelist1 = Routinelist(routine=routine1,
                           trainee=trainee3)
                           
session.add(routinelist1)
session.commit()

routinelist2 = Routinelist(routine=routine2,
                           trainee=trainee3)
                           
session.add(routinelist2)
session.commit()

routinelist3 = Routinelist(routine=routine1,
                           trainee=trainee4)
                           
session.add(routinelist3)
session.commit()

routinelist4 = Routinelist(routine=routine1,
                           trainee=trainee5)
                           
session.add(routinelist4)
session.commit()

routinelist5 = Routinelist(routine=routine2,
                           trainee=trainee5)
                           
session.add(routinelist5)
session.commit()

print "Data has been added to database!"