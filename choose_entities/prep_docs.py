import re
import sys
from collections import Counter
from pathlib import Path

import spacy
import textract

from choose_entities import logger

logger = logger.get_logger(__name__)


class PrepDocs:
    """Load pdf files from chosen directory and prepare the spacy docs.

    Attributes
    ----------
    path: PosixPath
        The path to the directory containing the pdf files.

    Methods
    -------
    prep_docs()
        Extract text and return spacy doc for each pdf in the directory.
    """

    def __init__(self, path):
        self.path = path

    def prep_docs(self):
        """Extract text and return spacy doc for each pdf in the directory."""

        dir_path = Path(self.path)
        files = list(dir_path.glob("*.pdf"))
        for file in files:
            text = textract.process(file)
            text = text.decode("utf-8", "ignore")
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text)
            yield doc


class LabelDocs:
    """Extract and organize entities and labels from the spacy docs.

    Attributes
    ----------
    docs: generator
        Spacy docs yielded from PrepDocs
    label_list: list
        List of tuples of ent and its label
    ents: list
        List of ent.text
    count: Counter
        Count of occurrences of each ent.text
    labels: list
        List of unique labels encountered
    index: dict
        Dictionary with labels as keys and ents as values
    inv_idx: dict
        Dictionary with ents as keys and labels as values

    Methods
    -------
    label_ents()
        Collect lists of ents and their labels from spacy docs.
    collect_ents()
        Extract ents from label_list.
    count_ents()
        Record total number of occurrences for each ent.text.
    seen_labels()
        Return list of unique entity labels.
    out_index()
        Return a dictionary of labels to ent.texts as strings.
    inv_index()
        Return a dictionary of ent.text to label.
    """

    def __init__(self, path):
        self.docs = PrepDocs(path).prep_docs()

        self.label_list = None
        self.ents = None
        self.count = None
        self.labels = None
        self.index = None
        self.inv_idx = None

    def label_ents(self):
        """Collect lists of ents and their labels from spacy docs.

        Returns
        -------
        label_list: list
            A list of tuples of the label and the ents belonging to that label.
        """

        self.label_list = [
            (ent.label_, ent.text)
            for doc in self.docs
            for ent in doc.ents
            if not ent.text.isspace()
        ]
        return self.label_list

    def collect_ents(self):
        """Extract ents from label_list."""
        self.ents = [re.sub(r"\n{1,}", " ", x[1]) for x in self.label_list]
        return self.ents

    def count_ents(self):
        """Record total number of occurrences for each ent.text."""
        ents = [x.strip() for x in self.ents]
        self.count = Counter(ents)

        return self.count

    def seen_labels(self):
        """Return list of unique entity labels."""
        self.labels = list(set([tup[0] for tup in self.label_list]))
        return self.labels

    def out_index(self):
        """Return a dictionary of labels to ent.texts as strings."""
        labels = self.label_list
        self.index = {}
        for tup in labels:
            if tup[0] not in self.index:
                self.index[tup[0]] = [re.sub(r"\n{1,}", " ", tup[1])]
            else:
                self.index[tup[0]].append(re.sub(r"\n{1,}", " ", tup[1]))
        return self.index

    def inv_index(self):
        """Return a dictionary of ent.text to label."""
        self.inv_idx = {v: k for k, values in self.index.items() for v in values}
        return self.inv_idx

    def run_label_docs(self):
        """Label docs and collect label metadata."""
        logger.info("Starting to label docs.")
        for stage in [
            self.label_ents,
            self.collect_ents,
            self.count_ents,
            self.seen_labels,
            self.out_index,
            self.inv_index,
        ]:
            try:
                stage()
            except Exception as err:
                logger.warning(err)
                raise err


def main(path):
    docs_labels = LabelDocs(path)
    return docs_labels.run_label_docs()


if __name__ == "__main__":
    main(sys.argv[1])
