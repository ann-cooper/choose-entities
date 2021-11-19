import pytest
import spacy

from choose_entities.prep_docs import PrepDocs


@pytest.fixture(scope="function")
def setup_docs():
    docs = list(PrepDocs("tests/sample_pdfs").prep_docs())
    return docs[0] if len(docs) == 1 else None


@pytest.mark.parametrize("vocab_len, type_check", [(1164, spacy.tokens.doc.Doc)])
def test_prep_docs(setup_docs, vocab_len, type_check):
    assert setup_docs.vocab.length == vocab_len
    assert isinstance(setup_docs, type_check) is True
