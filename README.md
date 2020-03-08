# choose-entities
PDF redaction preperation tool

### Create venv and run:
- python3 -m venv temp_env
- source temp_env/bin/activate
- python3 -m pip install -r requirements.txt 
- Download the English language model for Spacy: `python3 -m spacy download en`
- `python choose_entities/choose_ents.py path/to/pdf/directory`

### Run tests:
- Activate the venv and run `python3 -m pytest`
