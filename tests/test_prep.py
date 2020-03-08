import pytest

from tests import test_params


class TestPrepDocs:
    @pytest.mark.parametrize("vocab_len, type_check", test_params.prep_docs)
    def test_prep_docs(self, setup_docs, vocab_len, type_check):
        assert setup_docs.vocab.length == vocab_len
        assert isinstance(setup_docs, type_check) is True


class TestLabelDocs:
    @pytest.mark.parametrize("att, expected", test_params.label_docs)
    def test_label_docs(self, setup_labels, att, expected):
        test_dict = setup_labels.__dict__
        if isinstance(test_dict[att], list):
            actual = set(test_dict[att])
            expected = set(expected)
        else:
            actual = test_dict[att]
        assert actual == expected
