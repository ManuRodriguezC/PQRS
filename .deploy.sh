#!/bin/bash
NAME="pqrs"
PATHHOME="/home/ti/PQRS"
PATHDJANGO="$PATHHOME"
USER="ti"
GROUP="ti"
WORKERS=3
DJANGOWSGI="PQRS.wsgi"
IP=***.***.***.***
PORT=8005
LEVEL="debug"

ACCESS_LOG="/var/log/${NAME}_access.log"

echo "Starting $NAME"
cd $PATHDJANGO
pip install django --break-system-packages
pip install django-cors-headers --break-system-packages
pip install django-browser-reload --break-system-packages
pip install django-tailwind --break-system-packages
exec gunicorn $DJANGOWSGI --workers=$NWORKERS --user=$USER --group=$GROUP --log-level=$LEVEL --bind=$IP:$PORT --access-logfile=$ACCESS_LOG
