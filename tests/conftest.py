import pytest

from choose_entities.prep_docs import LabelDocs, PrepDocs


@pytest.fixture(scope="session", autouse=True)
def setup_docs():
    docs = list(PrepDocs("tests/sample_pdfs").prep_docs())
    return docs[0] if len(docs) == 1 else None


@pytest.fixture(scope="session", autouse=True)
def setup_labels():
    docs = LabelDocs("tests/sample_pdfs")
    return docs
