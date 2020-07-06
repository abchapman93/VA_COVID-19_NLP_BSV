from spacy.tokens import Doc

Doc.set_extension("cov_classification", default=None, force=True)


class DocumentClassifier:
    name = "document_classifier"

    def __init__(self):
        pass

    def classify_doc(self, doc):
        """Classify a document as either 'POS', 'UNK', or 'NEG'.
            - 'POS': there is at least one mention of COVID-19
                with a positive status and no excluding modifiers.
                Examples:
                    - "The patient is positive for COVID-19"
                    - "Her SARS-COV-2 results came back as DETECTED"
                    - "Pt admitted to hospital for COVID-19"
            - 'UNK': There is are no positive mentions of COVID-19
                and at least one non-excluded or uncertain mention.
                Examples:
                    - "Patient with suspicion for COVID-19."
                    - "Patient tested for COVID-19, results pending."
                    - "Cancelled appt due to COVID-19"
            - 'NEG': There are no positive, uncertain, or unasserted mentions.
                Examples:
                    - "The patient tested negative for SAS-COV-2"
                    - "He does not have novel coronavirus"
                    - "Patient presents for routine follow-up."
                    - "Visit done via telephone due to COVID-19 precautions"
        """
        excluded_ents = set()
        positive_ents = set()
        unasserted_ents = set()

        for ent in doc.ents:
            if ent.label_ != "COVID-19":
                continue
            # If the entity is negated, experienced by someone else,
            # Future/hypothetical, or marked as not relevant,
            # considered this entity to be 'excluded'
            if any(
                [
                    ent._.is_negated,
                    ent._.is_other_experiencer,
                    ent._.is_future,
                    ent._.is_not_relevant,

                ]
            ):
                excluded_ents.add(ent)
            # If it is 'positive' and not uncertain,
            # consider it to be a 'positive' ent
            elif ent._.is_positive and not ent._.is_uncertain:
                positive_ents.add(ent)
            # If either there are no excluding modifiers or it is
            # marked as 'uncertain', consider it 'unasserted
            else:
                unasserted_ents.add(ent)

        # If there is at least one 'positive' ent, return 'POS'
        # If there are only unasserted/uncertain, return 'UNK'
        # If there are no ents or only excluded ents, return 'NEG'
        if positive_ents:
            doc_classification = "POS"
        elif unasserted_ents:
            doc_classification = "UNK"
        else:
            doc_classification = "NEG"
        return doc_classification

    def __call__(self, doc):
        doc._.cov_classification = self.classify_doc(doc)

        return doc
