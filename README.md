# choose-entities
PDF redaction preperation tool

## Clone repo
- `git clone https://github.com/ann-cooper/choose-entities.git`

## Create venv locally
- To create a virtual environment in this project directory:
    - `cd choose-entities`
    - `python3 -m venv venv`
- Activate the venv: `source myenv/bin/activate`

## Install and run
```
pip install -r requirements/main.txt
pip install .
python3 -m spacy download en
```
- To run on the sample_pdfs dir:
- `python choose_entities/choose_ents.py tests/sample_pdfs/`

## Run tests:
- Activate the venv and run `python3 -m pytest`

## Managing dependencies
- Dependencies are managed with pip-tools.
- To update or change dependencies: activate the venv, then install pip-tools with `pip install pip-tools`
- Adjust the packages listed in requirements/main.in as needed.
- To re-output the main.txt: `pip-compile requirements/main.in --output-file=- > requirements/main.txt`
- To upgrade the packages: `pip-compile requirements/main.txt`
- To install the packages in your venv: `pip install -r requirements/main.txt`
