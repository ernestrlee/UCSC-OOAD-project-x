# Flask is a Python web development framework
# For info: http://flask.pocoo.org/
# Imports from flask
from flask import Flask, render_template, request, redirect, url_for, flash

# SQL Alchemy is a Python SQL toolkit
# Imports from sqlalchemmy
from sqlalchemy import create_engine, asc, or_, desc
from sqlalchemy.orm import sessionmaker

# Imports from database classes
from database_setup import Base, User, Trainee, Trainer, Exercise, Set, Routine
from database_setup import Routinelist, ExerciseRecord, PerformanceRecord

app = Flask(__name__)

# Connect to database and create database session
engine = create_engine('sqlite:///personaltrainer.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Global variables for form input
MUSCLE_GROUPS = ["abdominals", "arms", "back", "calves", "chest", "legs",
                 "shoulders"]
EXERCISE_TYPES = ["aerobic", "balance", "flexibility", "strength"]
DIFFICULTY = ["Easy", "Intermediate", "Hard", "Challenging"]


# Routes for root and home page
@app.route('/')
@app.route('/home/')
def showHome():
    return render_template('home.html')


# Route for login page
@app.route('/login/', methods=['GET', 'POST'])
def showLogin():
    # Get all trainee information from the database
    trainees = session.query(Trainee).all()
    # Get all trainer information from the database
    trainers = session.query(Trainer).all()

    # For post requests, log the user in as a trainer or trainee
    # and redirect to their home page once logged in
    if request.method == 'POST':
        # if the value of the dropdown is not empty
        if request.form['role']:
            # let role equal the value in the dropdown (trainer or trainee)
            role = request.form['role']
        if role == "trainer":
            # if the role is a trainer, get the email address and use the
            # email address to retrieve user data from the database
            if request.form['traineremail']:
                email = request.form['traineremail']
                user = session.query(User).filter_by(email=email).first()
            # redirect the user to the trainer's homepage
            return redirect(url_for('showTrainerHomepage', user_id=user.id))
        else:
            # if the role is a trainee, get the email address and use the
            # email address to retrieve user data from the database
            if request.form['traineeemail']:
                email = request.form['traineeemail']
                user = session.query(User).filter_by(email=email).first()
            # redirect the user to the trainee's homepage
            return redirect(url_for('showTraineeHomepage', user_id=user.id))

    # For get requests, show the login page passing the trainer and trainee
    # data so that the user can log into their account based on thier roles
    # and email address
    else:
        return render_template('login.html', trainers=trainers,
                               trainees=trainees)


# Route for registration page
@app.route('/registration/<string:role>/', methods=['GET', 'POST'])
def showRegistration(role):
    # For a post request, get the user information and store it into the
    # database, then redirect to the trainer/trainee's home page
    if request.method == 'POST':
        # Create a new user in the database
        newUser = User(name=request.form['name'],
                       email=request.form['email'],
                       password=request.form['password'],
                       birthdate=request.form['birthdate'],
                       image=request.form['image'])
        if newUser.image == "":
            newUser.image = "/static/images/profile.png"
        session.add(newUser)
        session.commit()

        # If the user is registering as a trainer
        if role == "trainer":
            # Create a new trainer in the database
            newTrainer = Trainer(years_experience=request.form['years'],
                                 gym=request.form['gym'],
                                 education=request.form['education'],
                                 specialization=request.form['specialization'],
                                 background=request.form['background'],
                                 user=newUser)
            session.add(newTrainer)
            session.commit()
            # Show a flash message to indicate registration was sucessful
            flash("Registration Successful")

            # Redirect the page to the trainer's homepage
            return redirect(url_for('showTrainerHomepage', trainer=newTrainer,
                            user_id=newUser.id))

        # If the user is registering as a trainee
        elif role == "trainee":
            # Create a new trainee in the database
            newTrainee = Trainee(goal=request.form['goal'],
                                 user=newUser)
            session.add(newTrainee)
            session.commit()
            flash("Registration Successful")

            # Redirect the page to the trainee's homepage
            return redirect(url_for('showTraineeHomepage', trainee=newTrainee,
                            user_id=newUser.id))

    else:
        # For get requests, show the registration page for the trainer
        if role == "trainer":
            return render_template('trainerregistration.html', role=role)
        # For get requests, show the registration page for the trainee
        else:
            return render_template('registration.html', role=role)


# Route for trainer home page
@app.route('/user/trainer/<int:user_id>/')
def showTrainerHomepage(user_id):
    # Get the user information from the database to show on the
    # home page
    user = session.query(User).filter_by(id=user_id).one_or_none()

    # If the user doesn't exist, show an error page
    if user is None:
        return "No user info exists for this user"

    # Get the trainer information from the database to show
    # on the home page
    trainer = session.query(Trainer).filter_by(user_id=user_id).one_or_none()

    # If the trainer doesn't exist, show an error page
    if trainer is None:
        return "No trainer page exists for this user"

    # Get a list of trainees that are under this trainer
    # to show on the home page
    trainees = (session.query(Trainee).filter_by(trainer_id=trainer.id)
                .order_by(desc(Trainee.id)).all())

    # Get a list of routines created by this trainer to show on
    # the homepage
    routines = (session.query(Routine).filter_by(creator_id=user_id)
                .order_by(desc(Routine.id)).all())

    # Load the HTML page and pass variables needed to render
    # the information on the page
    return render_template('trainerhome.html', user_id=user_id,
                           trainer=trainer, trainees=trainees,
                           routines=routines, user=user)


# Route for trainee home page
@app.route('/user/trainee/<int:user_id>/')
def showTraineeHomepage(user_id):
    # Get user information from the database to show
    # on the home page
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get trainee information from the database to show
    # on the home page
    trainee = session.query(Trainee).filter_by(user_id=user_id).one_or_none()
    if trainee is None:
        return "No trainee info exists for this user"

    # Get the trainee's routine list information to display
    # on the home page
    routine_list = (session.query(Routinelist).filter_by(trainee=trainee)
                    .order_by(desc(Routinelist.id)).limit(5).all())

    # Load the HTML page and pass variables needed to render
    # the information on the page
    return render_template('traineehome.html', user_id=user_id,
                           trainee=trainee, user=user,
                           routine_list=routine_list)


# Route for trainees to select trainers
@app.route('/user/trainee/<int:user_id>/trainers/', methods=['GET', 'POST'])
def selectTrainer(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get information for all trainers to display on the
    # trainer list page
    trainers = session.query(Trainer).all()

    # For post requests, update the trainee's trainer information on
    # the database, then redirect to the trainee homepage
    if request.method == 'POST':
        updateTrainee = session.query(Trainee).filter_by(user_id=user_id).one()
        if request.form['trainer_id']:
            updateTrainee.trainer_id = request.form['trainer_id']
        session.add(updateTrainee)
        session.commit()
        return redirect(url_for('showTraineeHomepage', user_id=user_id,
                                user=user))

    # For get requests, show the select trainer page
    else:
        return render_template('selecttrainer.html', trainers=trainers,
                               user_id=user_id, user=user)


# Route for trainers to view other trainers
@app.route('/user/trainer/<int:user_id>/trainers/')
def showTrainers(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get information for all trainers to display on the
    # trainer list page
    trainers = session.query(Trainer).all()
    return render_template('viewtrainers.html', trainers=trainers,
                           user_id=user_id, user=user)


# Route for editing the trainee profile
@app.route('/user/trainee/<int:user_id>/edit/', methods=['GET', 'POST'])
def editTrainee(user_id):
    # Get an instance of the current user's data
    editUser = session.query(User).filter_by(id=user_id).one_or_none()
    if editUser is None:
        return "No user info exists for this user"

    # Get an instance of the current trainee's data
    editTrainee = session.query(Trainee).filter_by(user_id=user_id).one()
    if editTrainee is None:
        return "No trainee info exists for this user"

    # For post requests, store the updated form data into the
    # database for the user and trainee objects, then redirect
    # to the trainee's home page
    if request.method == 'POST':
        if request.form['name']:
            editUser.name = request.form['name']
        if request.form['email']:
            editUser.email = request.form['email']
        if request.form['password']:
            editUser.password = request.form['password']
        if request.form['birthdate']:
            editUser.birthdate = request.form['birthdate']
        if request.form['image']:
            editUser.birthdate = request.form['image']
        session.add(editUser)
        session.commit()
        if request.form['goal']:
            editTrainee.goal = request.form['goal']
        session.add(editTrainee)
        session.commit()
        flash("Trainee profile has been updated")
        return redirect(url_for('showTraineeHomepage', user_id=user_id))

    # For get requests, show the edit trainee page
    else:
        return render_template('edittrainee.html', user_id=user_id,
                               user=editUser, trainee=editTrainee)


# Route for editing the trainer profile
@app.route('/user/trainer/<int:user_id>/edit/', methods=['GET', 'POST'])
def editTrainer(user_id):
    # Get an instance of the current user's data
    editUser = session.query(User).filter_by(id=user_id).one_or_none()
    if editUser is None:
        return "No user info exists for this user"

    # Get an instance of the current trainer's data
    editTrainer = session.query(Trainer).filter_by(user_id=user_id).one()

    # For post requests, store the updated form data into the
    # database for the user and trainer objects, then redirect
    # to the trainer's home page
    if request.method == 'POST':
        if request.form['name']:
            editUser.name = request.form['name']
        if request.form['email']:
            editUser.email = request.form['email']
        if request.form['password']:
            editUser.password = request.form['password']
        if request.form['birthdate']:
            editUser.birthdate = request.form['birthdate']
        if request.form['image']:
            editUser.image = request.form['image']
        session.add(editUser)
        session.commit()
        if request.form['years']:
            editTrainer.years_experience = request.form['years']
        if request.form['gym']:
            editTrainer.gym = request.form['gym']
        if request.form['education']:
            editTrainer.education = request.form['education']
        if request.form['specialization']:
            editTrainer.specialization = request.form['specialization']
        if request.form['background']:
            editTrainer.background = request.form['background']
        session.add(editTrainer)
        session.commit()
        flash("Trainer profile has been updated")
        return redirect(url_for('showTrainerHomepage', user_id=user_id))

    # For get requests, show the edit trainer page
    else:
        return render_template('edittrainer.html', user_id=user_id,
                               user=editUser, trainer=editTrainer)


# Route for a trainer to view exercises
@app.route('/user/trainer/<int:user_id>/exercises/')
def showExercises(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get a list of all exercises in the database to display
    # on the exercises page
    exercises = session.query(Exercise).all()
    return render_template('exercises.html', exercises=exercises,
                           user_id=user_id, user=user)


# Route for a trainee to view exercise details as a pop-up when
# viewing an exercise routine
@app.route('/user/exercises/<int:exercise_id>/')
def showExerciseDetail(exercise_id):
    # Get the exercise data from the database
    exercise = session.query(Exercise).filter_by(id=exercise_id).one_or_none()
    if exercise is None:
        return "Not able to find this exercise"

    return render_template('exercisedetail.html', exercise=exercise)


# Route for adding exercises
@app.route('/user/trainer/<int:user_id>/exercises/new',
           methods=['GET', 'POST'])
def addExercise(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # For a post request, create a new exercise object and gather all the
    # exercise information from the form and save it to the database
    if request.method == 'POST':
        musclegroups = ""
        exercisetypes = ""
        musclegroups = ", ".join(request.form.getlist('muscle_group'))
        exercisetypes = ", ".join(request.form.getlist('exercise_type'))
        newExercise = Exercise(name=request.form['name'],
                               description=request.form['desc'],
                               imageurl=request.form['image'],
                               videourl=request.form['video'],
                               body_parts=musclegroups,
                               type=exercisetypes,
                               creator_id=user_id)
        session.add(newExercise)
        session.commit()
        flash("Exercise \"%s\" was added." % newExercise.name)
        return redirect(url_for('showExercises', user_id=user_id))

    # For get requests, display the add exercise form
    else:
        return render_template('addExercise.html', muscle_groups=MUSCLE_GROUPS,
                               exercise_types=EXERCISE_TYPES, user_id=user_id,
                               user=user)


# Route for editing exercises
@app.route('/user/trainer/<int:user_id>/exercises/<int:exercise_id>/edit/',
           methods=['GET', 'POST'])
def editExercise(user_id, exercise_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get an instance of the selected exercise
    editExercise = session.query(Exercise).filter_by(id=exercise_id).one()
    if editExercise is None:
        return "Exercise not found"

    # Check if this trainer created the exercise before allowing to edit
    if editExercise.creator_id != user_id:
        return "You are not authorized to edit this exercise"

    # For a post request, store the information from the edit form
    # into the existing instance of the selected exercise
    if request.method == 'POST':
        editmusclegroups = ""
        editexercisetypes = ""
        editmusclegroups = ", ".join(request.form.getlist('muscle_group'))
        editexercisetypes = ", ".join(request.form.getlist('exercise_type'))

        if request.form['name']:
            editExercise.name = request.form['name']
        if request.form['desc']:
            editExercise.description = request.form['desc']
        if request.form['image']:
            editExercise.imageurl = request.form['image']
        if request.form['video']:
            editExercise.videourl = request.form['video']

        editExercise.body_parts = editmusclegroups
        editExercise.type = editexercisetypes
        session.add(editExercise)
        session.commit()
        flash("Exercise \"%s\" has been updated." % editExercise.name)
        return redirect(url_for('showExercises', user_id=user_id))

    # For get requests, display the edit exercise page
    else:
        return render_template('editExercise.html',
                               muscle_groups=MUSCLE_GROUPS,
                               exercise_types=EXERCISE_TYPES, user_id=user_id,
                               exercise_id=exercise_id, exercise=editExercise,
                               user=user)


# Route for deleting an exercises
@app.route('/user/trainer/<int:user_id>/exercises/<int:exercise_id>/delete/',
           methods=['GET', 'POST'])
def deleteExercise(user_id, exercise_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get an instance of the selected exercise
    exercise = session.query(Exercise).filter_by(id=exercise_id).one_or_none()
    if exercise is None:
        return "Exercise not found"

    # Check if this trainer created the exercise before allowing to delete
    if exercise.creator_id != user_id:
        return "You are not authorized to delete this exercise"

    # For a post request, delete the data from the database
    if request.method == 'POST':
        deleteExercise = (session.query(Exercise).filter_by(id=exercise_id)
                          .one())
        session.delete(deleteExercise)
        session.commit()
        flash("Exercise \"%s\" was deleted." % deleteExercise.name)
        return redirect(url_for('showExercises', user_id=user_id))

    # For a get request, show the delete confirmation page
    else:
        return render_template('deleteExercise.html', user_id=user_id,
                               exercise_id=exercise_id, exercise=exercise,
                               user=user)


# Route for a trainee to view their routine list
@app.route('/user/trainee/<int:user_id>/routines/')
def showTraineeRoutines(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"
    trainee = session.query(Trainee).filter_by(user_id=user_id).one_or_none()
    if trainee is None:
        return "No trainee info exists for this user"

    # Get the trainee's routine list
    routinelist = (session.query(Routinelist).filter_by(trainee_id=trainee.id)
                   .all())

    # Show the trainee's routine list
    return render_template('traineeroutines.html', routinelist=routinelist,
                           user_id=user_id, user=user)


# Route for viewing routines for trainers
@app.route('/user/trainer/<int:user_id>/routines/')
def showTrainerRoutines(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get a list of all routines from the database
    routines = session.query(Routine).all()

    # Get the data for the current trainer.
    trainer = session.query(Trainer).filter_by(user_id=user_id).one()

    # Show the routines page with all the routines
    return render_template('routines.html', routines=routines, user_id=user_id,
                           user=user, trainer=trainer)


# Route for showing a routine
@app.route('/user/trainer/<int:user_id>/routines/<int:routine_id>/')
def showRoutineSet(user_id, routine_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get data for the selected routine from the database
    routine = session.query(Routine).filter_by(id=routine_id).one_or_none()
    if routine is None:
        return "Routine was not found"

    # Get the data for all the sets that are part of the routine
    sets = session.query(Set).filter_by(routine_id=routine_id).all()

    # Show the page with the routine and set information
    return render_template('routinesets.html', routine=routine,
                           user_id=user_id, sets=sets, user=user)


# Route for showing routine details
@app.route('/user/routines/<int:routine_id>/')
def showRoutineDetail(routine_id):
    # Get the routine information from the database
    routine = session.query(Routine).filter_by(id=routine_id).one_or_none()
    if routine is None:
        return "Not able to find this routine"

    # Get set data from the database based on the routine chosen
    sets = session.query(Set).filter_by(routine_id=routine_id).all()

    # Show the routine detail page with the routine and set information
    return render_template('routinedetail.html', routine=routine, sets=sets)


# Route for adding a new a routine
@app.route('/user/trainer/<int:user_id>/routines/new/',
           methods=['GET', 'POST'])
def addRoutine(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get a list of all the exercises.  This is used to populate
    # a dropdown in the add routine page
    exercises = session.query(Exercise).all()

    # For a post request, get all the form information and store
    # it into the database
    if request.method == 'POST':
        # Create a new routine object and store it into the database
        newRoutine = Routine(name=request.form['name'],
                             difficulty=request.form['difficulty'],
                             description=request.form['desc'],
                             creator_id=user.id)
        session.add(newRoutine)
        session.commit()
        flash("New routine has been added.")

        # Create new set objects and add them to the routine object
        for i in range(1, 6):
            exercise = "exercise%s" % i
            rep = "rep%s" % i
            set = Set(order=i,
                      exercise_id=request.form[exercise],
                      repetitions=request.form[rep],
                      routine=newRoutine)
            session.add(set)
            session.commit()
            flash("A set was added to routine %s" % newRoutine.name)
        return redirect(url_for('showTrainerRoutines', user_id=user_id,
                        user=user))

    else:
        return render_template('addroutine.html', difficulty=DIFFICULTY,
                               exercises=exercises, user_id=user_id, user=user)


# Route for editing a routine
@app.route('/user/trainer/<int:user_id>/routines/<int:routine_id>/edit/',
           methods=['GET', 'POST'])
def editRoutine(user_id, routine_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get the data for all exercises to display as a drop down in the form
    exercises = session.query(Exercise).all()

    # Get an instance of the current routine selected for editing
    editRoutine = session.query(Routine).filter_by(id=routine_id).one_or_none()
    if editRoutine is None:
        return "Routine does not exist"

    # Check if the user is the creator of the routine
    # If not, show an error message
    if editRoutine.creator_id != user_id:
        return "You are not authorized to edit this routine"

    # Get an instance of all the sets in the routine
    editSets = session.query(Set).filter_by(routine_id=routine_id).all()

    # For post requests, get the form information and save the updated
    # data to the database
    if request.method == 'POST':
        if request.form['name']:
            editRoutine.name = request.form['name']
        if request.form['difficulty']:
            editRoutine.difficulty = request.form['difficulty']
        if request.form['desc']:
            editRoutine.description = request.form['desc']
        else:
            editRoutine.description = ""
        session.add(editRoutine)
        session.commit()
        flash("Routine '%s' has been updated." % editRoutine.name)

        # Save the updated set information to the database
        for i in range(1, 6):
            editSet = (session.query(Set).filter_by(routine_id=routine_id)
                       .filter_by(order=i).one_or_none())
            if editSet:
                exercise = "exercise%s" % i
                rep = "rep%s" % i
                if request.form[exercise]:
                    editSet.exercise_id = request.form[exercise]
                if request.form[rep]:
                    editSet.repetitions = request.form[rep]
                session.add(editSet)
                session.commit()
                flash("A set was updated in routine '%s'" % editRoutine.name)

        return redirect(url_for('showTrainerRoutines', user_id=user_id,
                        user=user))

    else:
        return render_template('editroutine.html', user_id=user_id,
                               routine_id=routine_id, routine=editRoutine,
                               sets=editSets, user=user, difficulty=DIFFICULTY,
                               exercises=exercises)


# Route for deleting a routine
@app.route('/user/trainer/<int:user_id>/routines/<int:routine_id>/delete/',
           methods=['GET', 'POST'])
def deleteRoutine(user_id, routine_id):
    # Get user information from the database
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get the routine that is going to be deleted
    routineToDelete = (session.query(Routine).filter_by(id=routine_id)
                       .filter_by(creator_id=user_id).one())
    routineName = routineToDelete.name

    # Check if the user is the creator of the routine
    # If not, show an error message
    if routineToDelete.creator_id != user_id:
        return "You are not authorized to delete this routine"

    # For a post request, delete the routine
    if request.method == 'POST':
        session.delete(routineToDelete)
        session.commit()

        # Show a flash message that the routine was deleted
        flash("Routine \"%s\" was deleted." % routineName)
        return redirect(url_for('showTrainerRoutines', user_id=user_id,
                        user=user))

    # For a get request, show the delete routine page
    else:
        return render_template('deleteroutine.html', user_id=user_id,
                               routine_id=routine_id, user=user,
                               routine=routineToDelete)


# Route for assigning a single routine to trainees
@app.route('/user/trainer/<int:user_id>/routines/<int:routine_id>/assign',
           methods=['GET', 'POST'])
def assignRoutineToTrainees(user_id, routine_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"
    trainer = session.query(Trainer).filter_by(user_id=user_id).one_or_none()
    if trainer is None:
        return "Trainer information not found"
    routine = session.query(Routine).filter_by(id=routine_id).one_or_none()
    if routine is None:
        return "No routine info found"
    # Get the data for all the trainees assigned to the trainer
    trainees = session.query(Trainee).filter_by(trainer_id=trainer.id).all()

    # For post requests, update the routine to each of the trainees
    if request.method == 'POST':
        # Get assigned trainees from checkbox fields on form
        assigned_trainee_ids = request.form.getlist('trainee')

        for id in assigned_trainee_ids:
            # Get all routines from the routine list that belong to
            # the trainee
            trainee_routine_list = (session.query(Routinelist)
                                    .filter_by(trainee_id=id).all())
            trainee = session.query(Trainee).filter_by(id=id).one_or_none()
            if trainee is None:
                return "Trainee not found"

            # Check to see if the routine is already on the trainee's list
            # If so, send a flash message
            for item in trainee_routine_list:
                if item.routine_id == routine_id:
                    flash("Routine '%s' already exists for %s" % (routine.name,
                          trainee.user.name))

            new_trainee_routine_list = Routinelist(routine=routine,
                                                   trainee=trainee)
            session.add(new_trainee_routine_list)
            session.commit()
            flash("Routine '%s' added to %s's routine list" % (routine.name,
                  trainee.user.name))

        flash("Routine %s added to trainees" % routine.name)
        return redirect(url_for('showTrainerRoutines', user_id=user_id,
                        user=user))
    else:
        return render_template('assignroutine.html', user_id=user_id,
                               routine_id=routine_id, user=user,
                               trainees=trainees, routine=routine)


# Route for assigning an individual trainee multiple routines
@app.route('/user/trainer/<int:user_id>/trainees/<int:trainee_id>/assign/',
           methods=['GET', 'POST'])
def assignTraineeRoutines(user_id, trainee_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"
    trainee = session.query(Trainee).filter_by(id=trainee_id).one_or_none()
    if trainee is None:
        return "No trainee info exists for this user"
    routines = session.query(Routine).all()
    # Get all the routines from the trainee selected
    current_trainee_routines = (session.query(Routinelist)
                                .filter_by(trainee_id=trainee.id).all())

    # Get the current routine ids in the trainee's list for setting as checked
    # in the form
    current_routines = []
    for current_routine in current_trainee_routines:
        current_routines.append(current_routine.routine_id)

    # For post requests, update the routine list for the trainee,
    # then redirect to the trainee list page
    if request.method == 'POST':
        # Get the id's from the selected checkbox in the form
        assigned_routine_ids = request.form.getlist('routine')

        # Delete the all the routines off the trainee's routine list
        delete_routines = (session.query(Routinelist)
                           .filter_by(trainee_id=trainee.id).all())
        for delete_routine in delete_routines:
            session.delete(delete_routine)
            session.commit()

        # Update the routine list for the trainee based on form data
        for routine_id in assigned_routine_ids:
            update_routine = Routinelist(routine_id=routine_id,
                                         trainee_id=trainee.id)
            session.add(update_routine)
            session.commit()
            flash("Routine '%s' added to %s's routine list" %
                  (update_routine.routine.name, trainee.user.name))

        return redirect(url_for('showTrainees', user_id=user_id, user=user))

    # For get requests, show the routine assignment page for the trainee
    else:
        return render_template('assigntraineeroutines.html', user_id=user_id,
                               user=user, trainee=trainee, routines=routines,
                               current_routines=current_routines)


# Route for peforming a routine
@app.route('/user/trainee/<int:user_id>/<int:routine_id>/perform',
           methods=['GET', 'POST'])
def performRoutine(user_id, routine_id):
    # Get user information from the database
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get trainee information from the database
    trainee = session.query(Trainee).filter_by(user_id=user_id).one_or_none()
    if trainee is None:
        return "No trainee info exists for this user"

    # Get routine information from the database
    routine = session.query(Routine).filter_by(id=routine_id).one_or_none()
    if routine is None:
        return "Routine info was not found"

    # Get set information from the database based on the routine
    sets = session.query(Set).filter_by(routine_id=routine_id).all()

    # For a post requests, create a new performance record and store
    #  the information to the database
    if request.method == 'POST':
        # Create a new performane record
        newRecord = PerformanceRecord(routine_name=routine.name,
                                      comments=request.form['comments'],
                                      rating=request.form['rating'],
                                      trainee_id=trainee.id)
        session.add(newRecord)
        session.commit()

        # Add exercise information to the performance record
        for set in sets:
            completed_rep = "completed%s" % set.order
            # Create a new exercise record
            if request.form[completed_rep]:
                exercise_record = ExerciseRecord(order=set.order,
                                                 exercise_name=set.exercise.name,
                                                 assigned_reps=set.repetitions,
                                                 completed_reps=request.form[completed_rep],
                                                 trainee_id=trainee.id,
                                                 performance_id=newRecord.id)
                session.add(exercise_record)
                session.commit()

        # Get data for all exerciese from the database
        exercises = session.query(ExerciseRecord).all()

        # Show a flash message that a record was added
        flash("Performance record has been added")
        return redirect(url_for('showPerformance', user_id=user_id, user=user,
                        exercises=exercises))

    # For get requests, show the perform routine screen
    else:
        return render_template('performroutine.html', user_id=user_id,
                               routine=routine, sets=sets, user=user)


# Route for showing a trainer's trainees
@app.route('/user/trainer/<int:user_id>/trainees/')
def showTrainees(user_id):
    # Get user information from the database
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get trainer information from the database
    trainer = session.query(Trainer).filter_by(user_id=user_id).one_or_none()
    if trainer is None:
        return "No trainer info for this trainer"

    # Get data for all trainees with the assigned trainer
    trainees = session.query(Trainee).filter_by(trainer_id=trainer.id).all()
    return render_template('traineelist.html', user_id=user_id,
                           trainees=trainees, user=user)


# Route for a trainee to view their performance
@app.route('/user/trainee/<int:user_id>/performance/')
def showPerformance(user_id):
    # Get user information from the database
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get trainee information from the database
    trainee = session.query(Trainee).filter_by(user_id=user_id).one_or_none()
    if trainee is None:
        return "No trainee info found for this trainee"

    # Get performance information from the database based on the trainee
    # and sort by latest datetime first
    performance = (session.query(PerformanceRecord)
                   .filter_by(trainee_id=trainee.id)
                   .order_by(desc(PerformanceRecord.performed_date)).all())

    # Get all exercises related to the trainee
    exercises = (session.query(ExerciseRecord)
                 .filter_by(trainee_id=trainee.id).all())

    return render_template('traineePerformance.html', user_id=user_id,
                           user=user, trainee=trainee, performance=performance,
                           exercises=exercises)


# Route for a trainer to view their trainee's performance
@app.route('/user/trainer/<int:user_id>/trainee/<int:trainee_id>/performance/')
def showTraineePerformance(user_id, trainee_id):
    # Get user information from the database
    user = session.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        return "No user info exists for this user"

    # Get trainee information from the database
    trainee = session.query(Trainee).filter_by(id=trainee_id).one_or_none()
    if trainee is None:
        return "No trainee info found for this trainee"

    # Get performance information from the database based on the trainee
    # and sort by latest datetime first
    performance = (session.query(PerformanceRecord)
                   .filter_by(trainee_id=trainee.id)
                   .order_by(desc(PerformanceRecord.performed_date)).all())

    # Get all exercises related to the trainee
    exercises = (session.query(ExerciseRecord)
                 .filter_by(trainee_id=trainee.id).all())

    return render_template('traineePerformance.html', user_id=user_id,
                           user=user, trainee=trainee, trainee_id=trainee_id,
                           performance=performance, exercises=exercises,
                           role="trainer")


if __name__ == '__main__':
    # Add secret key for flash messages
    app.secret_key = 'super_secret_key'
    # Reload server each time code changes
    app.debug = True
    # Run local server
    app.run(host='0.0.0.0', port=8000)
