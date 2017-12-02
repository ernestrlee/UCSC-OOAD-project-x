# UCSC-OOAD-project-x
Project X for OOAD class at UCSC, personal trainer app.  

This web application is designed to allow a trainee to perform exercise routines assigned to them by their trainer.  The personal trainer puts together exercise routines for their trainees using the app.  The trainee then performs the routine and enters information about the routine into the app.  The app allows the personal trainer to track the progress of their trainees based on the ability of their trainees to complete each of the exercises in a routine.  This way, the personal trainer is able to customize routines based on previous performance.

## File information:
* database_setup.py - sets up the database
* loadvalues.py - loads initial values to the database
* personaltrainer.py - the personal trainer web application

## Notes:
This app is a proof of concept.  As such certain items should be updated prior to deploying
* Login system is not fully functional and does not perform any authentication.
* Images that are used in the app are for demonstrative purposes only.
* App is in debug mode

## Setup instructions:

## Known issues:
When an exercise routine is deleted, the trainee is still left with a blank routine shown on their routine list.
