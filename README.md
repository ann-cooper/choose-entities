# choose-entities
PDF redaction preperation tool

## Clone repo
- `git clone https://github.com/ann-cooper/choose-entities.git`

## Create venv locally
- To create a virtual environment in this project directory:
    - `cd choose-entities`
    - `./create_venv.sh`
- Activate the venv: `source myenv/bin/activate`

## Add project to PYTHONPATH
- For example, in .bash_profile: `export PYTHONPATH=$PYTHONPATH:$HOME/<path_to_directory>`
- `source ~/.bash_profile`

## Run the chooser
- To run on the sample_pdfs dir:
- `python choose_entities/choose_ents.py tests/sample_pdfs/`

## Run tests:
- Activate the venv and run `pytest`
