# choose-entities
BitCurator PDF redaction

## Install Anaconda
1. download and [install miniconda](https://conda.io/en/latest/miniconda.html)
## Create conda enviroment
1. Either create the environment with the yaml file or create the environment manually.
2. To use the yaml file: [clone](https://help.github.com/en/articles/cloning-a-repository) or download the repo (or fork and clone the repo) to a local dir, "choose_ents" for example.
3. With the environment.yaml file at the top level of your local choose_ents directory (not within a sub-directory), open the terminal and run:  
`conda env create -f environment.yml`

2. To [create the environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) manually:
3. create new environment with python 2.7 `conda create -n choose_ents python=2.7`
3. activate the environment `source activate choose_ents`


### Conda environment requirements
4. download and install spacy and the english language model
5. install textract
6. install easygui

## To run the program:
1. open terminal and navigate to your choose_ents directory (make sure this makes sense, try both ways.)
2. `source activate choose_ents` to activate your environment
2. run the program with `python choose_ents.py path/to/your/pdfs`
3. This will start the program!
