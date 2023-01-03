Note: These instructions are based on the macOS.  If you have a Windows machine, you'll 
need to adapt these instructions for Windows.

## oTree

oTree is a framework based on Python and Django that lets you build single and multiplayer
strategy games, surveys, and quizzes.

Homepage: http://www.otree.org/

Live Demo: http://demo.otree.org/

Docs: http://otree.readthedocs.org

# Running the Sample Games in this Repo
The games in this Repo are built using a legacy version of oTree.  To run these games on 
your machine, you'll need to install oTree (2.3.10) and a legacy version of Python (3.7.15).  
It will be easier to set up and switch between versions of Python on your machine if you first 
install Anaconda.

### Install Anaconda and Python 3.7.15
Install Anaconda (macOS): https://docs.anaconda.com/anaconda/install/mac-os/

Open up the Terminal on your Mac, and enter the following commands:

```
conda create --name Py3715 python=3.7.15
conda activate Py3715
```

You should now see (Py3715) at the start of the command prompt.

### Install oTree 2.3.10
After activating your Python 3.7.15 virtual environment, enter the following commands:

```
pip3 install otree==2.3.10
```

### Download This Repository
Click the "Code" button above and select "Download ZIP."  Unzip the downloaded file, and 
you should see all of the folders/files from this repository on your local machine.

## Simple 3-Person Game: P-Beauty
This repo includes a simple implementation of a p-beauty contest (https://en.wikipedia.org/wiki/Guess_2/3_of_the_average).
Participants are matched into groups of 3.  On each trial, each participant guesses a number 
between 0 and 100.  The participant whose number is closest to 2/3 of the average of the three 
participants' chosen numbers is the winner.

This is a good place to start to get yourself oriented to the oTree framework before moving 
on to The Sales Game.

## The Sales Game
The other two games in this repository are versions of The Sales Game.  The Sales Game is a
20-armed bandit game comprised of 45 trials separated into three 15-trial Phases.  In each Phase
participants explore a different 20-armed bandit.  Participants must select exactly three arms
on each trial, and at the end of each trial the realized point value for each arm is revealed.

This repository contains a Solo version and a Social version of The Sales Game.  In the Solo 
version of the Game participants play alone without access to any side observations of the arm 
values.  In the Social version of the Game, participants are matched into groups of 3-6, and
have the option to share their results on each trial with the other members of their group. If
two members of a group both choose to share their results with each other, they are able to
view each other's results while making their selection on the next trial.  If either of a
pair choose not to share with the other, then neither of the participants may view the other's
results.

A video demonstration of the Social Sales Game functionality is available on YouTube:
https://www.youtube.com/watch?v=J5LWsjGL4sE

An in-depth description of the Solo and Social version of The Sales Game is available in 
Section 3.1 of Rao (2021), starting on page 18:
https://www.proquest.com/docview/2558047254?pq-origsite=gscholar&fromopenview=true

As of Jan 3, 2022, there are more robust annotations throughout the code for the Social 
version of The Sales Game.  You should start with the Solo version to get a sense of the 
Game dynamics, but if you get stuck, open the Social version to see if the annotations in 
that version of the code are helpful.

