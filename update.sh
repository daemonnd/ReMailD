#!/bin/bash

# def project folder
REMAILD_DIR=~/Documents/ReMailD

# checking if the folder exists
if [ ! -d "$REMAILD_DIR" ]; then
  echo "The directory '$REMAILD_DIR' doesn't exist."
  exit 1
fi

# change directory to project folder
cd "$REMAILD_DIR" || exit

# Checking if it is a git repository
if [ ! -d ".git" ]; then
  echo "This isn't a git repository. git will be init now."
  git init
  git remote add origin https://github.com/v01DaemonD/ReMailD.git
fi




# enter the commit meg
echo "Enter your commit message/the version: "
read COMMIT_MESSAGE

# adding changes to commit
git add .

# execute commit
git commit -m "$COMMIT_MESSAGE"

# push
git push origin main

# go to Documents Folder
cd ~/Documents

# msg that everything worked correctly 
echo "ReMailD have been saved and updated successfully!"
