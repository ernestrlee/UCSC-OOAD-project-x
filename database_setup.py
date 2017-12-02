# This file sets up a database with the table parameters below
import os
import sys
import datetime
# SQL Alchemy is a Python SQL toolkit
# Imports / Configuration for sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Table for user information
class User(Base):
    # Create the table name
    __tablename__ = 'user'

    # Map table columns to the table
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(12), nullable=False)
    birthdate = Column(String(12))
    image = Column(String)


# Table for trainer information
class Trainer(Base):
    __tablename__ = 'trainer'

    id = Column(Integer, primary_key=True)
    years_experience = Column(Integer)
    gym = Column(String(250))
    education = Column(String)
    specialization = Column(String)
    background = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


# Table for trainee information
class Trainee(Base):
    __tablename__ = 'trainee'

    id = Column(Integer, primary_key=True)
    goal = Column(String)
    trainer_id = Column(Integer, ForeignKey('trainer.id'))
    trainer = relationship(Trainer)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


# Table for exercise routine information
class Routine(Base):
    __tablename__ = 'routine'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String(500))
    difficulty = Column(String(80))
    creator_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    date_updated = Column(DateTime, onupdate=datetime.datetime.now)


# Table for trainee routines
class Routinelist(Base):
    __tablename__ = 'routinelist'

    id = Column(Integer, primary_key=True)
    routine_id = Column(Integer, ForeignKey('routine.id'))
    routine = relationship(Routine)
    trainee_id = Column(Integer, ForeignKey('trainee.id'))
    trainee = relationship(Trainee)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)


# Table for exercise information
class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(500))
    imageurl = Column(String)
    videourl = Column(String)
    type = Column(String(250))
    muscle_groups = Column(String)
    creator_id = Column((Integer), ForeignKey('user.id'))
    user = relationship(User)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    date_updated = Column(DateTime, onupdate=datetime.datetime.now)


# Table for set information
class Set(Base):
    __tablename__ = 'set'

    id = Column(Integer, primary_key=True)
    order = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    exercise = relationship(Exercise)
    routine_id = Column(Integer, ForeignKey('routine.id'))
    routine = relationship(Routine)


# Table for performance records
class PerformanceRecord(Base):
    __tablename__ = 'performancerecord'

    id = Column(Integer, primary_key=True)
    routine_name = Column(String, nullable=False)
    trainee_id = Column(Integer, nullable=False)
    comments = Column(String)
    rating = Column(Integer)
    performed_date = Column(DateTime, default=datetime.datetime.utcnow)


# Table for exercise records
class ExerciseRecord(Base):
    __tablename__ = 'exerciserecord'

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    exercise_name = Column(String(250))
    assigned_reps = Column(Integer)
    completed_reps = Column(Integer)
    trainee_id = Column(Integer, nullable=False)
    performance_id = Column(Integer, ForeignKey('performancerecord.id'))
    performancerecord = relationship(PerformanceRecord)


# Create an engine that stores data in the local directory's
# personaltrainer.db file.
engine = create_engine('sqlite:///personaltrainer.db')
# Create the database
Base.metadata.create_all(engine)
