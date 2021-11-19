from collections import Counter

import pytest

from choose_entities.prep_docs import LabelDocs


@pytest.fixture(scope="session")
def setup_labels():
    docs = LabelDocs("tests/sample_pdfs")
    docs.run_label_docs()
    return docs


def test_label_ents(setup_labels):
    assert all([isinstance(x, tuple) for x in setup_labels.label_list])
    assert len(setup_labels.label_list) == 63


def test_collect_ents(setup_labels):
    assert all([isinstance(x, str) for x in setup_labels.ents])
    assert len(setup_labels.ents) == len(setup_labels.label_list)


def test_count_ents(setup_labels):
    assert isinstance(setup_labels.count, Counter)
    assert len(setup_labels.count) == 50


def test_seen_labels(setup_labels):
    assert all([isinstance(x, str) for x in setup_labels.labels])
    assert len(setup_labels.labels) == 7


def test_out_index(setup_labels):
    assert isinstance(setup_labels.index, dict)
    assert list(setup_labels.index.keys()) == [
        "DATE",
        "PERSON",
        "QUANTITY",
        "CARDINAL",
        "ORG",
        "LOC",
        "GPE",
    ]


def test_inv_idx(setup_labels):
    assert isinstance(setup_labels.inv_idx, dict)
    assert set(setup_labels.inv_idx.values()) == set(setup_labels.index.keys())
