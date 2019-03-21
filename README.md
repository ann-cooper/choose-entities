# choose-entities
BitCurator PDF redaction

## Install Anaconda
1. Download and [install miniconda](https://conda.io/en/latest/miniconda.html)
## Create conda enviroment
2. To [create the environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) manually:
3. Create new environment with python 2.7 `conda create -n choose_ents python=2.7`
3. Activate the environment `conda activate choose_ents`

### Conda environment requirements
4. Install Spacy from conda: `conda install spacy==2.0.11` 
5. Pip install Textract: `pip install textract`
6. Pip install Easygui: `pip install easygui`
7. Download the English language model for Spacy: `python -m spacy download en`
8. If you don't want to run choose_entities right away, deactivate: `conda deactivate`

## To run the program:
1. Open terminal and navigate to your choose_ents directory.
2. `source activate choose_ents` to activate your environment.
2. Run the program with `python choose_ents.py path/to/your/pdfs`
3. This will start the program!
