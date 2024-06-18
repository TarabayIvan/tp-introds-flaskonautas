#!/bin/bash

mkdir .venv
pipenv install
pipenv run flask run -p 5000
