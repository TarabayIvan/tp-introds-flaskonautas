#!/bin/bash

mkdir .venv
pipenv install
pipenv shell
flask run -p 5000