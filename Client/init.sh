#!/bin/bash

cd static
cd images
mkdir posts-images
cd ..
cd ..
pipenv shell
pipenv install -r requirements.txt
flask run -p 5000