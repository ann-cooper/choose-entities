#!/bin/bash

python3 -m venv myenv
source myenv/bin/activate
python3 -m pip install poetry
python3 -m poetry install
# python3 -m pip install -r requirements.txt 
python3 -m spacy download en