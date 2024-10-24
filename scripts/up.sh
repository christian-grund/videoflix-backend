#!/bin/bash

# Nutzer nach Commit-Nachricht fragen
# echo "Enter commit message: "
# read commitMessage

# Git-Befehle ausführen
git add .
git commit -m "$*"
git push
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
ssh -A christian@34.159.98.222 "cd /home/grund7/projects/videoflix-backend/ && git pull"