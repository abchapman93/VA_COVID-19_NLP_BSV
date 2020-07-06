from medspacy.ner import TargetRule

target_rules = {
    "COVID-19": [
        # This will match basic COVID-19 concepts
        TargetRule(
            "<COVID-19>",
            "COVID-19",
            pattern=[{"_": {"concept_tag": "COVID-19"}, "OP": "+"}],
        ),
        # These will match more complex constructs
        # "Positive COVID-19"
        TargetRule(
            literal="<POSITIVE> <COVID-19>",
            category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "coronavirus"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "COVID-19 Positive"
        TargetRule(
            literal="<COVID-19> <POSITIVE>",
            category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # If COVID-19 is stated along with a specific diagnosis,
        # such as respiratory distress and pneumonia,
        # we'll count that to be positive
        # "COVID-19 + pneumonia"
        TargetRule(
            "<COVID-19> (<POSITIVE>)? <ASSOCIATED_DIAGNOSIS>",
            "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "*"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "COVID-19 pneumonia"
        TargetRule(
            "<ASSOCIATED_DIAGNOSIS> <COVID-19>",
            "COVID-19",
            pattern=[
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "Respiratory Distress with Pneumonia COVID-19"
        TargetRule(
            "<ASSOCIATED_DIAGNOSIS> with <ASSOCIATED_DIAGNOSIS> <COVID-19>",
            "COVID-19",
            pattern=[
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
                {"LOWER": {"IN": ["with", "w", "w/", "from"]}},
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "*"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "COVID-19 positive patient"
        TargetRule(
            "<COVID-19> positive <PATIENT>",
            "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "patient"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "COVID-19 + precautions"
        TargetRule(
            literal="<COVID-19> <POSITIVE> precautions",
            category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"LOWER": {"REGEX": "^precaution"}},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            literal="coronavirus positive screening",
            category="positive coronavirus screening",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "screening"}, "OP": "+"},
            ],
        ),
        TargetRule(
            literal="positive coronavirus screening",
            category="positive coronavirus screening",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "screening"}, "OP": "+"},
            ],
        ),
        TargetRule(
            literal="screening coronavirus positive",
            category="positive coronavirus screening",
            pattern=[
                {"_": {"concept_tag": "screening"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
            ],
        ),
        TargetRule(
            literal="screening positive coronavirus",
            category="positive coronavirus screening",
            pattern=[
                {"_": {"concept_tag": "screening"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
        ),
        # "Pneumonia due to COVID-19"
        TargetRule(
            literal="<ASSOCIATED_DIAGNOSIS> due to covid",
            category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
                {"LOWER": {"IN": ["due", "secondary"]}},
                {"LOWER": "to"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "<COVID-19> (XXX) DETECTED",
            "COVID-19",
            attributes={"is_positive": True},
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"TEXT": "("},
                {"TEXT": {"NOT_IN": [")"]}, "OP": "+"},
                {"TEXT": ")"},
                {"IS_SPACE": True, "OP": "*"},
                {"TEXT": {"REGEX": "(DETECTED|POSITIVE|^POS$)"}},
            ],
        ),
        TargetRule(
            "current covid-19 diagnosis",
            "COVID-19",
            attributes={"is_positive": True},
            pattern=[
                {"LOWER": {"IN": ["current", "recent"]}},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"IN": ["dx", "dx.", "diagnosis"]}},
            ],
        ),
        TargetRule(
            "<COVID-19> evaluation",
            "COVID-19",
            attributes={"is_uncertain": True},
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "eval"}},
            ],
        ),
        TargetRule(
            "<COVID-19> symptoms",
            "COVID-19",
            attributes={"is_uncertain": True},
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "symptom"}},
            ],
        ),
        TargetRule(
            "<PATIENT> has <COVID-19>",
            "COVID-19",
            attributes={"is_positive": True},
            pattern=[
                {"_": {"concept_tag": "patient"}, "OP": "+"},
                {"LEMMA": "do", "OP": "?"},
                {"LEMMA": "have"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
        ),
        TargetRule(
            "diagnosis: <COVID>",
            category="COVID-19",
            pattern=[
                {"LOWER": {"IN": ["diagnosis", "dx"]}},
                {"LOWER": ":"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "*"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "diagnosis: <COVID> testing",
            category="COVID-19",
            pattern=[
                {"LOWER": {"IN": ["diagnosis", "dx"]}},
                {"LOWER": ":"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "^(test|screen)"}},
            ],
        ),
        TargetRule(
            "diagnosis: <COVID> testing <POSITIVE>",
            category="COVID-19",
            pattern=[
                {"LOWER": {"IN": ["diagnosis", "dx"]}},
                {"LOWER": ":"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "^(test|screen)"}},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "COVID status: positive",
            "COVID-19",
            attributes={"is_positive": True},
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "status"},
                {"LOWER": ":"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
            ],
        ),
        TargetRule(
            "COVID related admission",
            "COVID-19",
            attributes={"is_positive": True},
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "-", "OP": "?"},
                {"LOWER": "related"},
                {"LOWER": "admission"},
            ],
        ),
        TargetRule(
            "admitted due to <COVID-19>",
            "COVID-19",
            attributes={"is_positive": True},
            pattern=[
                {"LOWER": "admitted"},
                {"LOWER": "due"},
                {"LOWER": "to"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
        ),
        TargetRule(
            "admitted with <COVID-19>",
            "COVID-19",
            attributes={"is_positive": True},
            pattern=[
                {"LOWER": "admitted"},
                {"LOWER": {"IN": ["with", "w", "w/"]}},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
        ),
        TargetRule(
            "COVID related <ASSOCIATED_DIAGNOSIS>",
            "COVID-19",
            attributes={"is_positive": True},
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "-", "OP": "?"},
                {"LOWER": "related"},
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
            ],
        ),
        TargetRule(
            "<COVID-19> infection",
            "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"LOWER": "infection"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "rule out <COVID-19>",
            "COVID-19",
            attributes={"is_uncertain": True},
            pattern=[
                {"LOWER": "rule"},
                {"LOWER": "out"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
        ),
        TargetRule(
            "<COVID-19> positive person",
            "COVID-19",
            attributes={"is_experienced": False},
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "other_experiencer"}, "OP": "+"},
                # {"LOWER": {"IN": ["person", "persons", "people", "patients"]}}
            ],
        ),
        TargetRule(
            "<COVID-19> <POSITIVE> unit",
            "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"LOWER": {"IN": ["unit", "floor"]}},
            ],
        ),
        TargetRule(
            "<POSITIVE> <COVID-19> unit",
            "COVID-19",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"IN": ["unit", "floor"]}},
            ],
        ),
        TargetRule(
            "active <COVID-19> precautions",
            "IGNORE",
            pattern=[
                {"LOWER": "active"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "precaution"}},
            ],
        ),
        TargetRule(
            "<POSITIVE> <COVID-19> exposure",
            "COVID-19",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"IN": ["exposure", "contact"]}},
            ],
        ),
        TargetRule(
            "known <COVID-19> exposure",
            "COVID-19",
            pattern=[
                {"LOWER": "known"},
                {"_": {"concept_tag": "positive"}, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "*"},
                {"LOWER": {"IN": ["exposure", "contact"]}},
            ],
        ),
        # If a relevant diagnosis code is in the text,
        # count it as positive
        TargetRule(
            literal="b34.2", category="COVID-19", attributes={"is_positive": True}
        ),
        TargetRule(
            literal="b342", category="COVID-19", attributes={"is_positive": True}
        ),
        TargetRule(
            literal="b97.29", category="COVID-19", attributes={"is_positive": True}
        ),
        TargetRule(
            literal="b97.29", category="COVID-19", attributes={"is_positive": True}
        ),
        TargetRule(
            literal="u07.1", category="COVID-19", attributes={"is_positive": True}
        ),
    ],
    # Extract antibody tests separately from other testing
    "antibody_test": [
        TargetRule(
            "antibody test",
            "antibody_test",
            pattern=[
                {"LOWER": {"IN": ["antibody", "antibodies", "ab"]}},
                {"LOWER": {"REGEX": "test"}},
            ],
        ),
    ],
    # Non-COVID coronaviruses for disambiguation
    "OTHER_CORONAVIRUS": [
        TargetRule(
            literal="other coronavirus",
            category="OTHER_CORONAVIRUS",
            pattern=[
                {"LOWER": {"REGEX": "coronavirus|hcovs?|ncovs?|^covs?"}},
                {"TEXT": "-", "OP": "?"},
                {"LOWER": "infection", "OP": "?"},
                {"LOWER": "strain", "OP": "?"},
                {"IS_SPACE": True, "OP": "?"},
                {
                    "LOWER": {
                        "IN": [
                            "229e",
                            "229",
                            "oc43",
                            "oc",
                            "o43",
                            "0c43",
                            "oc-43",
                            "43",
                            "nl63",
                            "hku1",
                            "hkut1",
                            "hkui",
                            "emc",
                            "nl63",
                            "nl65 ",
                            "nl",
                            "63",
                            "hku-1",
                        ]
                    }
                },
            ],
        ),
        TargetRule(
            literal="other coronavirus",
            category="OTHER_CORONAVIRUS",
            pattern=[
                {
                    "LOWER": {
                        "IN": [
                            "229e",
                            "229",
                            "oc43",
                            "oc",
                            "o43",
                            "0c43",
                            "oc-43",
                            "43",
                            "nl63",
                            "hku1",
                            "hkut1",
                            "hkui",
                            "emc",
                            "nl63",
                            "nl65 ",
                            "nl",
                            "63",
                            "hku-1",
                        ]
                    }
                },
                {"LOWER": {"REGEX": "coronavirus|hcovs?|ncovs?|^covs?"}},
            ],
        ),
        TargetRule(
            literal="non-covid coronavirus",
            category="OTHER_CORONAVIRUS",
            pattern=[
                {"LOWER": "non"},
                {"LOWER": "-", "OP": "?"},
                {"LOWER": {"IN": ["novel", "covid", "ncovid", "covid-19"]}},
                {"LOWER": "coronavirus", "OP": "?"},
            ],
        ),
        TargetRule(
            literal="noncovid",
            category="OTHER_CORONAVIRUS",
            pattern=[{"LOWER": {"REGEX": "noncovid"}}],
        ),
    ],
    "coronavirus screening": [
        TargetRule(
            literal="[{'TEXT': '+'}, {'LOWER': 'covid-19'}, {'LOWER': {'REGEX': 'screen'}}]",
            category="coronavirus screening",
            pattern=[
                {"TEXT": "+"},
                {"LOWER": "covid-19"},
                {"LOWER": {"REGEX": "screen"}},
            ],
        ),
        TargetRule(
            literal=" positive COVID-19 Screening", category="coronavirus screening"
        ),
        TargetRule(literal="COVID-19 Screening", category="coronavirus screening"),
    ],
    # The following rules will extract phrases which may be confused with other concepts.
    # To explicitly exclude them, we'll extract them as "IGNORE", which will then be removed
    # in postprocessing
    "IGNORE": [
        TargetRule(
            literal="coronvirus pandemic",
            category="IGNORE",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}},
                {
                    "LEMMA": {
                        "IN": [
                            "restriction",
                            "emergency",
                            "epidemic",
                            "outbreak",
                            "crisis",
                            "breakout",
                            "pandemic",
                            "spread",
                        ]
                    }
                },
            ],
        ),
        TargetRule(
            literal="coronavirus screening",
            category="IGNORE",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}},
                {"LOWER": {"IN": ["screen", "screening", "screenings"]}},
            ],
        ),
        TargetRule(
            literal="droplet precautions",
            category="IGNORE",
            pattern=[
                {"LOWER": {"REGEX": "droplet"}},
                {"LOWER": "isolation", "OP": "?"},
                {"LOWER": {"REGEX": "precaution"}},
            ],
        ),
        TargetRule(
            literal="contact precautions",
            category="IGNORE",
            pattern=[{"LOWER": "contact"}, {"LOWER": {"REGEX": "precaution"}}],
        ),
        TargetRule(
            literal="positive for influenza",
            category="IGNORE",
            pattern=[
                {"LOWER": "positive"},
                {"LOWER": "for", "OP": "?"},
                {"LOWER": {"IN": ["flu", "influenza"]}},
            ],
        ),
        TargetRule(
            literal="positive patients",
            category="IGNORE",
            pattern=[
                {"LOWER": "positive"},
                {"LOWER": {"IN": ["people", "patients", "persons"]}},
            ],
        ),
        TargetRule(
            literal="confirm w/",
            category="IGNORE",
            pattern=[
                {"LEMMA": "confirm"},
                {"LOWER": {"IN": ["with", "w", "w/"]}},
                {"TEXT": "/", "OP": "?"},
            ],
        ),
        TargetRule(
            literal="the positive case",
            category="IGNORE",
            pattern=[
                {"LOWER": "the"},
                {"LOWER": "positive"},
                {"OP": "?"},
                {"LEMMA": "case"},
            ],
        ),
        TargetRule(literal="positive cases", category="IGNORE"),
        TargetRule(
            literal="results are confirmed",
            category="IGNORE",
            pattern=[
                {"LOWER": "results"},
                {"LOWER": "are", "OP": "?"},
                {"LOWER": "confirmed"},
            ],
        ),
        TargetRule(
            literal="exposed to <POSITIVE>",
            category="IGNORE",
            pattern=[
                {"LOWER": "exposed"},
                {"LOWER": "to"},
                {"_": {"concept_tag": "positive"}},
            ],
        ),
        TargetRule(
            literal="negative/positive pressure",
            category="IGNORE",
            pattern=[{"LOWER": {"REGEX": "^(neg|pos)"}}, {"LOWER": "pressure"}],
        ),
        TargetRule(literal="a positive case", category="IGNORE"),
        TargetRule(literal="positive attitude", category="IGNORE"),
        TargetRule(literal="[ ] COVID-19", category="IGNORE"),
        TargetRule(literal="positive feedback", category="IGNORE"),
        TargetRule(
            literal="Has patient been diagnosed with",
            category="IGNORE",
            pattern=[
                {"LOWER": "has"},
                {"LOWER": "the", "OP": "?"},
                {"LOWER": "patient"},
                {"LOWER": "been"},
                {"LOWER": "diagnosed"},
                {"LOWER": {"IN": ["with", "w", "w/"]}},
            ],
        ),
        TargetRule(literal="people with confirmed covid-19", category="IGNORE"),
        TargetRule(literal="positive serology", category="IGNORE"),
        TargetRule(literal="patients with confirmed covid-19", category="IGNORE"),
        TargetRule(
            literal="covid positive individuals",
            category="COVID-19",
            attributes={"is_experiencer": False},
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"LOWER": "tested", "OP": "?"},
                {"_": {"concept_tag": "other_experiencer"}, "OP": "+"},
                # {"LOWER": {"IN": ["individual", "individuals", "contact", "contact", "patients", "pts"]}}
            ],
        ),
        TargetRule("age 65 +", "IGNORE"),
        TargetRule("age 65+", "IGNORE"),
        TargetRule("return to work", "IGNORE"),
        TargetRule("back to work", "IGNORE"),
        TargetRule(
            "in order to decrease the spread of the COVID-19 infection", "IGNORE"
        ),
        TargetRule(
            "<COVID-19> guidelines",
            "IGNORE",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "guidelines"},
            ],
        ),
        TargetRule(
            "<COVID-19> rate",
            "IGNORE",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "infection", "OP": "?"},
                {"LEMMA": "rate"},
            ],
        ),
    ],
    "OTHER_PERSON": [
        TargetRule(
            literal="<COVID-19> <POSITIVE> <PERSON>",
            category="OTHER_PERSON",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"LOWER": {"IN": ["patients", "persons", "people", "veterans"]}},
            ],
        ),
        TargetRule(
            literal="positive covid individuals",
            category="COVID-19",
            attributes={"is_experiencer": False},
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "tested", "OP": "?"},
                {"_": {"concept_tag": "other_experiencer"}, "OP": "+"},
            ],
        ),
        TargetRule(
            literal="<POSITIVE> <COVID-19> <PERSON>",
            category="OTHER_PERSON",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LEMMA": {"IN": ["patients", "persons", "people", "veterans"]}},
            ],
        ),
        TargetRule(
            literal="contact with a <POSITIVE> <COVID-19>",
            category="OTHER_PERSON",
            pattern=[
                {"LOWER": {"IN": ["contact", "exposure"]}},
                {"LOWER": {"IN": ["with", "to"]}},
                {"OP": "?"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {
                    "LEMMA": {
                        "IN": ["patients", "persons", "people", "veterans", "patient"]
                    }
                },
            ],
        ),
        TargetRule(
            literal="patient who tested positive for",
            category="OTHER_PERSON",
            pattern=[
                {"LEMMA": {"IN": ["patient", "person", "pt", "pt."]}},
                {"LOWER": {"IN": ["who", "that"]}},
                {"LEMMA": "test"},
                {"LOWER": {"IN": ["positive", "confirmed", "+"]}},
                {"LOWER": "for"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
        ),
    ],
}
