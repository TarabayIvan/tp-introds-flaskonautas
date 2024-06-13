#!/bin/bash

if [ $# -ne 2];then
    exit 1
fi
puerto=$1
app=$2

export FLASK_DEBUG=1
export FLASK_APP="$app"

flask run --port="$puerto"


