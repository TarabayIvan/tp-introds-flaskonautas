#!/bin/bash

pipenv shell
pipenv install -r requirements.txt
flask run -p 5001