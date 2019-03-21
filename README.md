# choose-entities
BitCurator PDF redaction

## Install Anaconda
- Download and [install miniconda](https://conda.io/en/latest/miniconda.html)

## Create conda enviroment
- Create new environment with python 2.7 `conda create -n choose_ents python=2.7`
- Activate the environment `conda activate choose_ents`

### Conda environment requirements
- Install Spacy from conda: `conda install spacy==2.0.11` 
- Pip install Textract: `pip install textract`
- Pip install Easygui: `pip install easygui`
- Download the English language model for Spacy: `python -m spacy download en`
- If you don't want to run choose_entities right away, deactivate: `conda deactivate`

## To run:
- Open terminal and navigate to your choose_ents directory.
- `source activate choose_ents` to activate your environment.
- Run the program with `python choose_ents.py path/to/your/pdfs`
