import pytest

import cov_bsv

nlp = cov_bsv.load()

class TestMedSpaCy:

    def test_default_load(self):

        expected_pipe_names = ['tagger',
         'parser',
         'concept_tagger',
         'target_matcher',
         'sectionizer',
         'context',
         'postprocessor',
         'document_classifier']
        assert nlp.pipe_names == expected_pipe_names

    def test_common_terms(self):
        expected_ents = ["COVID-19", "SARS-COV-2", "novel coronavirus 2019", "ncov-19"]
        # text = ("He has COVID-19. "
        #         "Came in to be tested for SARS-COV-2. "
        #         "Heard about the novel coronavirus 2019. "
        #         "Is negative for ncjov-19")
        docs = list(nlp.pipe(expected_ents))
        for doc in docs:
            assert doc.text == doc.ents[0].text

    def test_simple_classifications(self):
        texts = [
            "He is positive for COVID-19.",
            "She is negative for COVID-19.",
            "This has COVID-19 but no assertion.",
        ]
        docs = list(nlp.pipe(texts))
        expected_classifications = ["POS", "NEG", "UNK"]
        for doc, expected in zip(docs, expected_classifications):
            assert doc._.cov_classification == expected
