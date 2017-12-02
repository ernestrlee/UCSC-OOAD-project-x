# UCSC-OOAD-project-x
Project X for OOAD class at UCSC, personal trainer app.  

This web application is designed to allow a trainee to perform exercise routines assigned to them by their trainer.  The personal trainer puts together exercise routines for their trainees using the app.  The trainee then performs the routine and enters information about the routine into the app.  The app allows the personal trainer to track the progress of their trainees based on the ability of their trainees to complete each of the exercises in a routine.  This way, the personal trainer is able to customize routines based on previous performance.

## File information:
* database_setup.py - sets up the database
* loadvalues.py - loads initial values to the database
* personaltrainer.py - the personal trainer web application

## How to install

1. Start by installing Python 2 to your system.  For the latest version, please visit the [Python website](https://www.python.org/).

2. Install a command line tool such as [Git BASH](https://git-for-windows.github.io/).

3. A virtual machine (VM) must also be installed to run the web server.  For this project, Vagrant and VirtualBox were used.
Files can be found from the links below:
    * https://www.virtualbox.org/wiki/Downloads
    * https://www.vagrantup.com/downloads.html 

4. Configure the the VM using files that can be found in the below link:
    - https://github.com/udacity/fullstack-nanodegree-vm

5. Download the files from this Git repository and place them into the same folder.  Make sure the files are in the same path as the virtual machine files.
    * personaltrainer.py
    * database_setup.py
    * loadvalues.py
    * static folder (and all it's contents)
    * templates folder (and all it's contents)

## How to setup the web server
Follow the below instructions to set up the web server.
1. Run the command line tool, such as Git Bash.
2. Start your virtual machine.  If using Vagrant, this is usually done by using the `vagrant up` command followed by `vagrant ssh`.
3. Navigate to the directory that contains the "personaltrainer.py" file.
4. Using Python, run the file, "database_setup.py".  For example, `python database_setup.py`.  This will set up an sqlite database, "personaltrainer.db".
5. Next, run the file "loadvalues.py".  For example, `python loadvalues.py`.  This will initially populate the database with information.
6. To start the web server, run the item catalog file "personaltrainer.py".  For example `python personaltrainer.py`.  This will start the web server on local host 8000.
7. Finally, open a browser and type the address into the browser. `localhost:8000`

## Notes:
This app is a proof of concept.  As such certain items should be updated prior to deploying
* Login system is not fully functional and does not perform any authentication.
* Images that are used in the app are for demonstrative purposes only.
* App is in debug mode and should be turned off prior to deploying

## Known issues:
When an exercise routine is deleted, the trainee is still left with a blank routine shown on their routine list.
