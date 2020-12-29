from medspacy.context import ConTextRule
from . import callbacks

context_rules = [
    # "NEGATED_EXISTENCE" will be used to negate entities
    # ie., "COVID-19 not detected"
    ConTextRule(
        literal="Not Detected",
        category="NEGATED_EXISTENCE",
        direction="BACKWARD",
        pattern=[
            {"LOWER": {"IN": ["not", "non"]}},
            {"IS_SPACE": True, "OP": "*"},
            {"TEXT": "-", "OP": "?"},
            {"LOWER": {"REGEX": "detecte?d"}},
        ],
        # Limit to 1 since this phrase occurs in tabular data like:
        # "CORONAVIUS 229E Not Detected CORONAVIRUS HKU1 Detected"
        # max_scope=3, # Set a small window, but allow for whitespaces
        max_targets=1,
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        ": negative",
        "NEGATED_EXISTENCE",
        direction="BACKWARD",
        max_scope=3,  # Set a small window, but allow for whitespaces
        max_targets=1,
    ),
    ConTextRule("not been detected", "NEGATED_EXISTENCE", direction="BACKWARD"),
    ConTextRule("none detected", "NEGATED_EXISTENCE", direction="BACKWARD"),
    ConTextRule("free from", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule(
        "not tested",
        "NEGATED_EXISTENCE",
        direction="BACKWARD",
        pattern=[{"LOWER": "not"}, {"LOWER": "been", "OP": "?"}, {"LOWER": "tested"}],
    ),
    ConTextRule(
        "Ref Not Detected",
        "IGNORE",
        direction="TERMINATE",
        pattern=[
            {"LOWER": "ref"},
            {"LOWER": ":"},
            {"LOWER": "not"},
            {"LOWER": "detected"},
        ],
        max_targets=1,
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "not indicated", "NEGATED_EXISTENCE", direction="BACKWARD", max_scope=5
    ),
    ConTextRule(
        "NEGATIVE NEG",
        "NEGATED_EXISTENCE",
        direction="BACKWARD",  # Lab results
        pattern=[{"TEXT": "NEGATIVE"}, {"IS_SPACE": True, "OP": "*"}, {"TEXT": "NEG"}],
        max_scope=1,
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "negative screen",
        "NEGATED_EXISTENCE",
        direction="BIDIRECTIONAL",
        max_scope=2,
    ),
    ConTextRule(
        "negative test", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL", max_scope=4
    ),
    ConTextRule(
        "without any", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=2
    ),
    ConTextRule("denies", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=10),
    ConTextRule(
        "denies any", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=10
    ),
    ConTextRule(
        "denies travel", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=10
    ),
    ConTextRule("denied", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=10),
    ConTextRule("no evidence", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule(
        "history of",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        max_scope=4,
        pattern=[
            {"LOWER": "no"},
            {"LOWER": {"IN": ["hx", "-hx", "history"]}},
            {"LOWER": "of"},
        ],
    ),
    ConTextRule(
        "no diagnosis of",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"OP": "?"},
            {"LOWER": {"IN": ["dx", "diagnosis"]}},
            {"LOWER": "of", "OP": "?"},
        ],
    ),
    ConTextRule(
        "no", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=2
    ),  # Limit to a small scope
    ConTextRule("no positive", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("no one", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("no residents", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule(
        "no confirmed cases",
        "NEGATED_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": "no"}, {"LOWER": "confirmed"}, {"LEMMA": "case"}],
    ),
    ConTextRule(
        "not been confirmed",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        max_scope=2,
        pattern=[
            {"LOWER": {"IN": ["not", "n't"]}},
            {"LOWER": "been", "OP": "?"},
            {"LOWER": "confirmed"},
        ],
    ),
    ConTextRule("no known", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=5),
    ConTextRule(
        "no contact with",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        max_scope=None,
        pattern=[
            {"LOWER": "no"},
            {"OP": "?"},
            {"LOWER": "contact"},
            {"LOWER": {"REGEX": "w/?(ith)?$"}, "OP": "?"},
        ],
    ),
    ConTextRule(
        "answer no",
        "NEGATED_EXISTENCE",
        direction="BIDIRECTIONAL",  # "Veteran answered no to being exposed to coronavirus"
        pattern=[
            {"LOWER": {"REGEX": "^answer"}},
            {"TEXT": '"', "OP": "?"},
            {"LOWER": {"IN": ["no", "negative", "neg"]}},
            {"TEXT": '"', "OP": "?"},
        ],
    ),
    ConTextRule("negative", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL",),
    ConTextRule(
        "negative for",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": {"IN": ["negative", "neg"]}}, {"LOWER": "for"}],
    ),
    # ConTextRule("is negative for", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("not positive", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL"),
    ConTextRule(
        "excluded", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL", max_scope=4
    ),
    ConTextRule(
        "no risk factors for",
        "UNCERTAIN",
        "FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": "no"},
            {"LOWER": "risk"},
            {"LEMMA": "factor"},
            {"LOWER": "for"},
        ],
    ),
    ConTextRule(
        "negative screening for",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": "negative"},
            {"LOWER": {"REGEX": "screen"}},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextRule(
        "screening negative",
        "NEGATED_EXISTENCE",
        direction="BACKWARD",
        pattern=[{"LOWER": {"REGEX": "^screen"}}, {"LOWER": {"REGEX": "^neg"}}],
    ),
    ConTextRule(
        "screened negative for",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "^screen"}},
            {"LOWER": {"REGEX": "^neg"}},
            {"LOWER": "for"},
        ],
    ),
    ConTextRule("does not screen positive", "NEGATED_EXISTENCE"),
    ConTextRule(
        "is negative",
        "NEGATED_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[{"LEMMA": "be"}, {"LOWER": "negative"}],
    ),
    ConTextRule(
        "not test positive", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL"
    ),
    ConTextRule(
        "no screening for",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "not?"}},
            {"LOWER": {"REGEX": "^screen"}},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextRule("no signs of", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule(
        "no symptoms",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": "no"}, {"LOWER": {"REGEX": "(sign|symptom)"}}],
    ),
    ConTextRule(
        "no testing for",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "^no"}},
            {"LOWER": {"REGEX": "^test"}},
            {"LOWER": "for"},
        ],
    ),
    ConTextRule(
        "no indication of",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"LOWER": {"REGEX": "indication"}},
            {"LOWER": {"IN": ["of", "for"]}, "OP": "?"},
        ],
    ),
    ConTextRule(
        "no exposure",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": "no"}, {"LOWER": {"REGEX": "^exposure"}}],
    ),
    ConTextRule(
        "without signs/symptoms",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": "without"},
            {"OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms"]}},
            {"LOWER": "or", "OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms"]}, "OP": "?"},
        ],
    ),
    ConTextRule(
        "w/o signs/symptoms",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": "w/o"},
            {"OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms"]}},
            {"LOWER": "or", "OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms"]}, "OP": "?"},
        ],
    ),
    ConTextRule(
        "does not have any signs/symptoms",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        pattern=[
            {"LOWER": "does"},
            {"LOWER": {"IN": ["not", "n't"]}},
            {"LOWER": "have"},
            {"LOWER": "any", "OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms", "ss", "s/s"]}},
        ],
    ),
    ConTextRule("not have", "NEGATED_EXISTENCE", max_scope=5),
    ConTextRule(
        "not have a <POSITIVE>? diagnosis",
        "NEGATED_EXISTENCE",
        pattern=[
            {"LOWER": {"IN": ["not", "n't"]}},
            {"LOWER": "have"},
            {"LOWER": "a"},
            {"_": {"concept_tag": "positive"}, "OP": "*"},
            {"_": {"concept_tag": "diagnosis"}, "OP": "+"},
        ],
    ),
    ConTextRule("no evidence of", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule(
        "does not meet criteria", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL"
    ),
    ConTextRule(
        "no concern for",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"LOWER": "concern"},
            {"LOWER": {"IN": ["for", "of"]}},
        ],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "not at risk",
        "NEGATED_EXISTENCE",
        "FORWARD",
        pattern=[{"LOWER": "not"}, {"LOWER": "at"}, {"LOWER": "risk"}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "no risk",
        "NEGATED_EXISTENCE",
        "FORWARD",
        pattern=[{"LOWER": "no"}, {"OP": "?"}, {"LOWER": "risk"}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "no suspicion",
        "NEGATED_EXISTENCE",
        "FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"LOWER": {"REGEX": "^suspicion"}},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextRule("not suspect", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("not", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=4),
    ConTextRule(
        "ruled out for",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "is ruled out",
        "NEGATED_EXISTENCE",
        direction="BACKWARD",
        pattern=[
            {"LOWER": {"IN": ["is", "are", "were"]}},
            {"OP": "?", "POS": "ADV"},
            {"LOWER": "ruled"},
            {"LOWER": "out"},
        ],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "does not meet criteria",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "is not likely",
        "NEGATED_EXISTENCE",
        direction="BACKWARD",
        pattern=[
            {"LOWER": {"IN": ["is", "are"]}},
            {"LOWER": "not"},
            {"LOWER": "likely"},
        ],
    ),
    ConTextRule(
        "no travel",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": "no"}, {"LOWER": "recent", "OP": "?"}, {"LOWER": "travel"}],
    ),
    ConTextRule(
        "not be in",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        allowed_types={"location", "COVID-19"},
    ),
    ConTextRule(
        "cleared from",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "^clear"}},
            {"LOWER": {"IN": ["of", "for", "from"]}},
        ],
    ),
    ConTextRule(
        "no history of travel",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"LOWER": {"IN": ["hx", "history"]}},
            {"LOWER": "of", "OP": "?"},
            {"LOWER": "travel"},
        ],
        allowed_types={"location", "COVID-19"},
    ),
    ConTextRule(
        "no exposure to",
        "NEGATED_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": "no"}, {"OP": "?"}, {"LOWER": "exposure"}, {"LOWER": "to"}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "no contact with",
        "NEGATED_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": "no"}, {"OP": "?"}, {"LEMMA": "contact"}, {"LOWER": "with"}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "not have contact with",
        "NEGATED_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": "not"},
            {"LOWER": "have"},
            {"OP": "?"},
            {"LOWER": "contact"},
            {"LOWER": "with"},
        ],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "no X contacts",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"IN": ["no", "any"]}},
            {"LOWER": "known", "OP": "?"},
            {"OP": "?"},
            {"LEMMA": "contact"},
            {"LOWER": "with", "OP": "?"},
        ],
    ),
    ConTextRule(
        "anyone with", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=None
    ),
    ConTextRule(
        "no symptoms of",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19"},
    ),
    ConTextRule(
        "no risk factors",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19"},
    ),
    ConTextRule(
        "no confirmed cases",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19"},
    ),
    ConTextRule(
        "does not meet screening criteria",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": "does"},
            {"LOWER": {"IN": ["not", "n't"]}},
            {"LOWER": "meet"},
            {"LOWER": "screening", "OP": "?"},
            {"LOWER": "criteria", "OP": "?"},
            {"LOWER": "for", "OP": "?"},
        ],
        allowed_types={"COVID-19"},
    ),
    ConTextRule(": no", "NEGATED_EXISTENCE", direction="BACKWARD", max_scope=4),
    ConTextRule(
        "no report",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": "no"}, {"LOWER": {"REGEX": "report"}}],
    ),
    ConTextRule(
        "not diagnosed with",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        max_scope=2,
        pattern=[
            {"LOWER": {"IN": ["not", "never"]}},
            {"OP": "?"},
            {"LOWER": "diagnosed"},
            {"LOWER": "with"},
        ],
    ),
    ConTextRule(
        "not been tested or diagnosed with",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        max_scope=2,
    ),
    ConTextRule(
        "not been tested for or diagnosed with",
        "NEGATED_EXISTENCE",
        direction="FORWARD",
        max_scope=2,
    ),
    ConTextRule(
        "not tested positive for",
        "NEGATED_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": "not"},
            {"LOWER": {"REGEX": "^test"}},
            {"_": {"concept_tag": "positive"}, "OP": "+"},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextRule("not tested", "NEGATED_EXISTENCE", direction="FORWARD",),
    ConTextRule(
        "not tested or diagnosed", "NEGATED_EXISTENCE", direction="FORWARD",
    ),

    # "DEFINITE_POSITIVE_EXISTENCE" will be used to set is_positive to True
    ConTextRule(
        "confirmed",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BIDIRECTIONAL",
        on_match=callbacks.disambiguate_confirmed,
        max_scope=2,  # Too ambiguous of a word, needs to be very close
    ),
    ConTextRule("known", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=2),
    ConTextRule(
        "positive for",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": {"IN": ["pos", "positive", "+"]}}, {"LOWER": "for"}],
    ),
    ConTextRule(
        "positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BIDIRECTIONAL",
        on_match=callbacks.disambiguate_positive,
    ),
    ConTextRule(
        "pos status", "DEFINITE_POSITIVE_EXISTENCE", direction="BACKWARD", max_scope=3
    ),
    ConTextRule(
        "results are positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BACKWARD",
        max_scope=3,
        pattern=[
            {"LOWER": {"REGEX": "result"}},
            {"LOWER": {"IN": ["is", "are"]}},
            {"LOWER": "positive"},
        ],
    ),
    ConTextRule(
        "pos", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL", max_scope=5
    ),
    ConTextRule(
        "results pos", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL", max_scope=5
    ),
    ConTextRule("positivity", "DEFINITE_POSITIVE_EXISTENCE", direction="BACKWARD"),
    ConTextRule(
        "test +",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^test"}},
            {"LOWER": {"IN": ["positive", "pos", "+", "(+)"]}},
        ],
    ),
    ConTextRule("+ve", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL",),
    ConTextRule(
        "(+)",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[{"TEXT": {"IN": ["(+)", "+"]}}],
        max_scope=1,
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS", "sign/symptom"},
    ),
    ConTextRule(
        "(+)",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[{"TEXT": {"IN": ["(+)", "+"]}}, {"LOWER": "for"}],
        max_scope=1,
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "test remains positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BACKWARD",
        pattern=[
            {"LOWER": {"IN": ["test", "pcr"]}},
            {"LOWER": "remains"},
            {"LOWER": {"IN": ["pos", "positive", "+", "(+)"]}},
        ],
    ),
    ConTextRule(
        "notified of positive results",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "notif(y|ied)"}},
            {"OP": "?"},
            {"LOWER": "of"},
            {"_": {"concept_tag": "positive"}, "OP": "+"},
            {"LOWER": {"REGEX": "results?|test(ing)?|status"}},
        ],
    ),
    ConTextRule(
        "notified the veteran of positive results",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "notif(y|ied)"}},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": {"IN": ["veteran", "patient", "family"]}},
            {"LOWER": "of"},
            {"_": {"concept_tag": "positive"}, "OP": "+"},
            {"LOWER": {"REGEX": "results?|test(ing)?|status"}},
        ],
    ),
    ConTextRule(
        "likely secondary to",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        max_scope=1,
    ),
    ConTextRule(
        "Problem:", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=10
    ),
    ConTextRule(
        "PROBLEM LIST:", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=10
    ),
    ConTextRule(
        "current problems:", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=10
    ),
    ConTextRule(
        "Problem List of", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=10
    ),
    ConTextRule(
        "active problems:", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=10
    ),
    ConTextRule(
        "acute problems", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=10
    ),
    ConTextRule(
        "admission diagnosis:",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "admi(t|ssion)"}},
            {"LOWER": {"IN": ["diagnosis", "dx", "dx."]}},
            {"LOWER": ":", "OP": "?"},
        ],
    ),
    ConTextRule(
        "Reason for admission:",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        max_scope=4,
    ),
    ConTextRule(
        "treatment of", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=4
    ),
    ConTextRule(
        "Admitting Diagnosis:",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        max_scope=4,
        pattern=[
            {"LOWER": "admitting", "OP": "?"},
            {"LOWER": {"IN": ["diagnosis", "dx", "dx."]}},
        ],
    ),
    ConTextRule("dx:", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=4,),
    ConTextRule(
        "diagnosed <DATE>",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BACKWARD",
        max_scope=4,
        pattern=[
            {"LOWER": {"REGEX": "(diagnos|dx)(ed)?"}},
            {"LOWER": {"REGEX": "[\d]{1,2}/[\d]{1,2}"}},
        ],
    ),
    ConTextRule("Reason for admission:", "ADMISSION", direction="FORWARD", max_scope=6,),
    ConTextRule("inpatient with", "ADMISSION", direction="FORWARD", max_scope=6,),
    ConTextRule("discharged from", "ADMISSION", direction="FORWARD", max_scope=6,),
    ConTextRule(
        "diagnosed with", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=6,
    ),
    ConTextRule(
        "found to be positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BACKWARD",
        max_scope=6,
    ),
    ConTextRule(
        "found to be positive for",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        max_scope=6,
    ),
    ConTextRule("+ test", "DEFINITE_POSITIVE_EXISTENCE",),
    ConTextRule(
        "in icu for",
        "ADMISSION",
        direction="FORWARD",
        max_scope=6,
        pattern=[
            {"LOWER": "in"},
            {"LOWER": {"REGEX": "^m?icu"}},
            {"LOWER": {"IN": ["for", "with"]}},
        ],
    ),
    ConTextRule(
        "admitted <DATE>",
        "ADMISSION",
        direction="FORWARD",
        pattern=[
            {"LEMMA": "admit", "POS": "VERB"},
            {"LOWER": {"REGEX": "^[\d]{1,2}/[\d]{1,2}"}},
        ],
    ),
    ConTextRule(
        "admitted with",
        "ADMISSION",
        direction="FORWARD",
        max_scope=None,
        pattern=[
            {"LOWER": {"REGEX": "admit"}, "POS": "VERB"},
            {"LOWER": {"IN": ["with", "for"]}},
        ],
    ),
    ConTextRule("admitted to", "ADMISSION", direction="FORWARD",),
    ConTextRule("admitted on", "ADMISSION", direction="FORWARD"),
    ConTextRule(
        "Reason for ED visit or Hospital Admission:",
        "ADMISSION",
        direction="FORWARD",
        max_scope=2,
    ),
    ConTextRule("Reason for ICU:", "ADMISSION", direction="FORWARD"),
    ConTextRule(
        "in the hospital for for",
        "ADMISSION",
        direction="FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"IN": ["in", "to"]}},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": {"IN": ["hospital", "icu", "micu"]}},
            {"LOWER": "for"},
        ],
    ),
    ConTextRule(
        "in the hospital due to",
        "ADMISSION",
        direction="FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"IN": ["in", "to"]}},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": {"IN": ["hospital", "icu", "micu"]}},
            {"LOWER": "due"},
            {"LOWER": "to"},
        ],
    ),
    ConTextRule(
        "hospitalized for",
        "ADMISSION",
        direction="FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"REGEX": "hospitali"}},
            {"_": {"concept_tag": "timex"}, "OP": "*"},
            {"LOWER": "for"},
        ],
    ),
    ConTextRule(
        "hospitalized due to",
        "ADMISSION",
        direction="FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"REGEX": "hospitali"}},
            {"_": {"concept_tag": "timex"}, "OP": "*"},
            {"LOWER": "due"},
            {"LOWER": "to"},
        ],
    ),
    ConTextRule("admission for", "ADMISSION", direction="FORWARD"),
    ConTextRule(
        "management of", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=3
    ),
    ConTextRule(
        "history of travel",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"IN": ["hx", "-hx", "history"]}},
            {"LOWER": "of"},
            {"LOWER": "travel"},
        ],
        allowed_types={"location"},
    ),
    ConTextRule(
        "presumed positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^presum"}},
            {"LOWER": {"IN": ["pos", "positive", "+"]}, "OP": "?"},
        ],
    ),
    ConTextRule(
        "ARDS from",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": "ards"}, {"LOWER": {"IN": ["from", "with"]}, "OP": "?"}],
        allowed_types={"COVID-19"},
        max_scope=3,
    ),
    ConTextRule(
        "ARDS secondary to",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": "ards"}, {"LOWER": "secondary"}, {"LOWER": "to"}],
        allowed_types={"COVID-19"},
        max_scope=3,
    ),
    ConTextRule(
        "acute respiratory distress",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        max_scope=3,
    ),
    ConTextRule(
        "post-extubation", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=3
    ),
    ConTextRule(
        "in the setting of",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
        pattern=[
            {"LOWER": "in"},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": "setting"},
            {"LOWER": "of"},
        ],
    ),
    ConTextRule(
        "in the s/o",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
    ),
    ConTextRule(
        "found to have",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
    ),
    ConTextRule(
        "presents with",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
        pattern=[{"LOWER": {"REGEX": "^present"}, "POS": "VERB"}, {"LOWER": "with"}],
    ),
    ConTextRule(
        "respiratory failure",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "resp"}},
            {"LOWER": "failure"},
            {"LOWER": {"IN": ["with", "due"]}, "OP": "?"},
            {"LOWER": "to", "OP": "?"},
        ],
        max_scope=4,
    ),
    ConTextRule(
        "respiratory failure 2/2",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "resp"}},
            {"LOWER": "failure"},
            {"LOWER": "(", "OP": "?"},
            {"LOWER": {"REGEX": "[12]/2"}},
            {"LOWER": ")", "OP": "?"},
        ],
        max_scope=4,
    ),
    ConTextRule(
        "active for",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": "active"}, {"LOWER": "for", "OP": "?"}],
        allowed_types={"COVID-19"},
        max_scope=2,
        on_match=callbacks.disambiguate_active,
    ),
    ConTextRule(
        "resolving", "DEFINITE_POSITIVE_EXISTENCE", direction="BACKWARD", max_scope=2
    ),
    ConTextRule(
        "recovering from",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[{"LOWER": {"IN": ["recovery", "recovering"]}}, {"LOWER": "from"}],
        max_scope=2,
    ),
    ConTextRule(
        "not recovered",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        pattern=[
            {"LOWER": "not"},
            {"LOWER": "yet", "OP": "?"},
            {"LOWER": {"REGEX": "^recover"}},
        ],
    ),
    ConTextRule(
        "Detected",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BACKWARD",
        max_targets=1,
        max_scope=5,
        pattern=[{"LOWER": {"REGEX": "^detected"}}],
        on_match=callbacks.check_no_x_detected,
    ),
    ConTextRule(
        "Value: Detected",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BACKWARD",
        max_targets=1,
        max_scope=5,
        pattern=[
            {"LOWER": "value"},
            {"LOWER": ":"},
            {"LOWER": {"REGEX": "^detected"}},
        ],
        on_match=callbacks.check_no_x_detected,
    ),
    ConTextRule(
        "POSITIVEH",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="BACKWARD",
        max_targets=1,
        max_scope=5,
    ),
    # "PATIENT_EXPERIENCER" modifiers will set is_positive to True
    # These will capture constructs such as "76-year-old male admitted for COVID-19"
    ConTextRule(
        "<NUM> yo with",
        "PATIENT_EXPERIENCER",
        direction="FORWARD",
        pattern=[
            {"LIKE_NUM": True},
            {"LOWER": "-", "OP": "?"},
            {"LOWER": "year"},
            {"LOWER": "-", "OP": "?"},
            {"LOWER": "old"},
            # Optionally allow race, ie., "76-year-old **white** male with COVID-19"
            {
                "LOWER": {"IN": ["aa", "white", "black", "hispanic", "caucasian"]},
                "OP": "?",
            },
            {
                "OP": "?",
                "_": {"concept_tag": {"NOT_IN": ["family", "other_experiencer"]}},
            },
            {"LOWER": {"IN": ["with", "w", "w/", "admitted",]}},
        ],
        max_scope=10,
    ),
    ConTextRule(
        "<NUM> yo with",
        "PATIENT_EXPERIENCER",
        direction="FORWARD",
        pattern=[
            {"LIKE_NUM": True},
            {"LOWER": {"REGEX": "y[or]"}},
            {
                "OP": "?",
                "_": {"concept_tag": {"NOT_IN": ["family", "other_experiencer"]}},
            },  # "male/female/..."
            {"LOWER": {"IN": ["patient", "veteran"]}, "OP": "?"},
            {"LOWER": {"IN": ["with", "w", "w/"]}},
        ],
        max_scope=10,
    ),
    ConTextRule(
        "<NUM> y/o with",
        "PATIENT_EXPERIENCER",
        direction="FORWARD",
        pattern=[
            {"LIKE_NUM": True},
            {"LOWER": "y"},
            {"LOWER": "/"},
            {"LOWER": "o"},
            {"OP": "?"},  # "male/female/..."
            {"LOWER": {"IN": ["patient", "veteran"]}, "OP": "?"},
            {"LOWER": {"IN": ["with", "w", "w/"]}},
        ],
        max_scope=10,
    ),
    ConTextRule(
        "<NUM>yo with",
        "PATIENT_EXPERIENCER",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "[\d]+yo"}},
            {"OP": "?"},  # "male/female/..."
            {"LOWER": {"IN": ["patient", "veteran"]}, "OP": "?"},
            {"LOWER": {"IN": ["with", "w", "w/"]}},
        ],
        max_scope=10,
    ),
    ConTextRule(
        "the patient has",
        "PATIENT_EXPERIENCER",
        direction="FORWARD",
        max_scope=3,
        pattern=[
            {"LOWER": "the"},
            {"LOWER": {"IN": ["veteran", "vet", "patient", "pt"]}},
            {"LOWER": "has"},
        ],
    ),
    # "FUTURE/HYPOTHETICAL" will mark is_hypothetical to True
    # This will capture cases where the patient doesn't actually have COVID-19
    # but are instead talking about precautions, general information, etc.
    ConTextRule(
        "precaution",
        "FUTURE/HYPOTHETICAL",
        direction="BACKWARD",
        max_scope=2,
        pattern=[{"LOWER": {"REGEX": "precaution"}}],
    ),
    ConTextRule("precautions:", "IGNORE", direction="FORWARD", max_scope=2),
    ConTextRule(
        "precaution for",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "precaution|protection|protect"}},
            {"LOWER": {"IN": ["for", "against"]}},
        ],
    ),
    ConTextRule("concern about", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule("reports of", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule(
        "vaccine",
        "FUTURE/HYPOTHETICAL",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),  # If they're talking about vaccines, it's probably just the patient asking
    ConTextRule("protect yourself", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule(
        "prevention",
        "FUTURE/HYPOTHETICAL",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^prevent"}}],
    ),
    ConTextRule("avoid", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule(
        "questions about",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "question"}},
            {"LOWER": {"IN": ["about", "regarding", "re", "concerning", "on", "for"]}},
        ],
        allowed_types={"COVID-19"},
    ),
    ConTextRule(
        "information about",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        max_scope=3,
        allowed_types={"COVID-19"},
        pattern=[{"LOWER": "information"}, {"LOWER": {"IN": ["about", "regarding"]}}],
    ),
    ConTextRule("anxiety about", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule(
        "ask about",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        pattern=[{"LOWER": {"REGEX": "^ask"}}, {"LOWER": "about"}],
        allowed_types={"travel", "COVID-19"},
    ),
    ConTextRule(
        "education",
        "FUTURE/HYPOTHETICAL",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^educat"}}],
    ),
    ConTextRule(
        "instruction",
        "FUTURE/HYPOTHETICAL",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "instruction"}}],
    ),
    ConTextRule(
        "information about",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        max_scope=3,
        pattern=[
            {"LOWER": "information"},
            {"LOWER": {"IN": ["on", "about", "regarding", "re"]}, "OP": "?"},
        ],
    ),
    ConTextRule("materials", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL",),
    ConTextRule("factsheet", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL",),
    ConTextRule("fact sheet", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL",),
    ConTextRule("protocol", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL", max_scope=3),
    ConTextRule("literature", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL"),
    ConTextRule(
        "handout",
        "FUTURE/HYPOTHETICAL",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^informat"}, "OP": "?"},
            {"LOWER": {"IN": ["handout", "handouts"]}},
        ],
    ),
    ConTextRule(
        "anxious about",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"IN": ["anxious", "worried", "worries", "worry", "worrying"]}},
            {"LOWER": {"IN": ["about", "re", "regarding"]}, "OP": "?"},
        ],
        allowed_types={"COVID-19",},
    ),
    ConTextRule(
        "if", "FUTURE/HYPOTHETICAL", direction="FORWARD", max_scope=10
    ),  # "If COVID-19 test is positive"
    ConTextRule(
        "advisory",
        "SCREENING",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["advisory", "advisories"]}}],
    ),
    ConTextRule("travel screen", "SCREENING", direction="BIDIRECTIONAL"),
    ConTextRule("travel screen:", "SCREENING", direction="BIDIRECTIONAL"),
    ConTextRule("Travel History Questionnaire", "SCREENING", direction="BIDIRECTIONAL"),
    ConTextRule("questionnaire:", "SCREENING", direction="BACKWARD", max_scope=2),
    ConTextRule(
        "questionnaire",
        "SCREENING",
        direction="BACKWARD",
        max_scope=2,
        pattern=[{"LOWER": {"REGEX": "questionn?aire"}}],
    ),
    ConTextRule(
        "questions",
        "SCREENING",
        direction="BACKWARD",
        max_scope=2,
        pattern=[{"LEMMA": "question"}],
    ),
    ConTextRule(
        "screening",
        "SCREENING",
        direction="BIDIRECTIONAL",
        max_scope=10,
        pattern=[{"LOWER": {"REGEX": "^screen"}}],
    ),
    ConTextRule(
        "prescreening",
        "SCREENING",
        direction="BIDIRECTIONAL",
        max_scope=None,
        pattern=[{"LOWER": {"REGEX": "prescreen"}}],
    ),
    ConTextRule("front gate", "SCREENING", direction="BIDIRECTIONAL",),
    ConTextRule("have you", "NOT_RELEVANT", direction="FORWARD",),
    # ConTextRule
    ConTextRule(
        "This patient was screened for the following suspected travel related illness(es):",
        "FUTURE/HYPOTHETICAL",
        direction="BIDIRECTIONAL",
    ),
    ConTextRule(
        "will be traveling",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        allowed_types={"location", "COVID-19"},
        pattern=[
            {"LOWER": "will"},
            {"LOWER": "be", "OP": "?"},
            {"LOWER": {"REGEX": "travel"}},
        ],
    ),
    ConTextRule(
        "travel plans",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        allowed_types={"location", "COVID-19"},
    ),
    ConTextRule(
        "if you need", "FUTURE/HYPOTHETICAL", direction="FORWARD"
    ),  # "If you need to be tested for"
    ConTextRule(
        "limit risk of",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        pattern=[
            {"LEMMA": {"IN": ["limit", "reduce", "lower", "minimize"]}},
            {"LOWER": "the", "OP": "?"},
            {"LEMMA": {"IN": ["risk", "chance", "possibility"]}},
            {"LEMMA": "of"},
        ],
    ),  # "If you need to be tested for"
    ConTextRule(
        "plan to travel",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        allowed_types={"location", "COVID-19"},
        pattern=[
            {"LOWER": {"REGEX": "plan"}},
            {"LOWER": "to"},
            {"LOWER": {"REGEX": "travel"}},
        ],
    ),
    ConTextRule(
        "N years ago",
        "HISTORICAL",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LIKE_NUM": True, "OP": "?"},
            {"LOWER": {"IN": ["year", "years"]}},
            {"LOWER": "ago"},
        ],
    ),
    # Previously, these modifiers were set to be "HISTORICAL"
    # but are instead being marked as "POSITIVE" so that we identify any current
    # or past cases of COVID-19.
    ConTextRule(
        "history of",
        "DEFINITE_POSITIVE_EXISTENCE",
        direction="FORWARD",
        max_scope=4,
        pattern=[{"LOWER": {"IN": ["hx", "-hx", "history"]}}, {"LOWER": "of"}],
    ),
    ConTextRule(
        "(resolved)", "DEFINITE_POSITIVE_EXISTENCE", direction="BACKWARD", max_scope=1
    ),
    # ConTextRule("resolved", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL", max_scope=3),
    # ConTextRule("20XX", "HISTORICAL", direction="BIDIRECTIONAL", max_scope=5,
    #             pattern=[{"TEXT": {"REGEX": "20[01][0-8]"}}]),
    ConTextRule(
        "in 20XX",
        "HISTORICAL",
        direction="BIDIRECTIONAL",
        max_scope=5,
        pattern=[{"LOWER": "in"}, {"OP": "?"}, {"TEXT": {"REGEX": "^20[01][0-9]$"}}],
    ),
    # The following modifiers try to capture instances where a health department
    # or infection control team was contacted
    ConTextRule(
        "contacted",
        "COMMUNICATION",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["contacted", "contact"]}, "POS": "VERB"}],
        allowed_types={"health department"},
        # on_match=callbacks.di,
    ),  # TODO: may have to disambiguate this with "came in contact"
    ConTextRule(
        "contact",
        "CONTACT",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": "contact", "POS": "NOUN"}],
        allowed_types={"COVID-19"},
        on_match=callbacks.disambiguate_contact,
    ),
    ConTextRule(
        "call",
        "COMMUNICATION",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^call"}}],
        allowed_types={"health department"},
    ),
    ConTextRule(
        "was contacted",
        "COMMUNICATION",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["was", "been"]}}, {"LOWER": "contacted"}],
        allowed_types={"health department"},
    ),
    ConTextRule(
        "notified",
        "COMMUNICATION",
        direction="BIDIRECTIONAL",
        allowed_types={"health department"},
    ),
    ConTextRule(
        "communicate with",
        "COMMUNICATION",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^communicate"}},
            {"LOWER": {"IN": ["with", "w"]}},
            {"LOWER": "/", "OP": "?"},
        ],
        allowed_types={"health department"},
    ),
    ConTextRule(
        "sent to",
        "COMMUNICATION",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": "sent"}, {"OP": "?"}, {"LOWER": "to"}],
        allowed_types={"health department"},
    ),
    ConTextRule(
        "sent",
        "COMMUNICATION",
        direction="BIDIRECTIONAL",
        allowed_types={"health department"},
    ),
    ConTextRule(
        "spoke with",
        "COMMUNICATION",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": "spoke"}, {"LOWER": {"IN": ["with", "to"]}}],
        allowed_types={"health department"},
    ),
    ConTextRule(
        "consulted",
        "COMMUNICATION",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "consult"}}, {"LOWER": "with", "OP": "?"}],
        allowed_types={"health department"},
    ),
    ConTextRule(
        "test for",
        "TEST",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^test"}}, {"LOWER": "for", "OP": "?"}],
    ),
    ConTextRule(
        "retest for",
        "TEST",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^retest"}}, {"LOWER": "for", "OP": "?"}],
    ),
    ConTextRule(
        "check for",
        "TEST",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^check"}, "POS": "VERB"}, {"LOWER": "for"}],
    ),
    ConTextRule(
        "work up",
        "TEST",
        pattern=[{"LOWER": "work"}, {"LOWER": "-", "OP": "?"}, {"LOWER": "up"}],
    ),
    ConTextRule("workup", "TEST"),
    ConTextRule("results", "TEST", "BACKWARD", max_scope=2),
    ConTextRule(
        "evaluation",
        "TEST",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=2,
    ),
    ConTextRule(
        "evaluated for",
        "TEST",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^eval"}}, {"LOWER": "for"}],
    ),
    ConTextRule(
        "swab",
        "TEST",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^swab"}}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "PCR",
        "TEST",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "specimen sent",
        "TEST",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule("awaiting results", "UNCERTAIN", direction="BIDIRECTIONAL"),
    ConTextRule(
        "at risk for",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "risk for",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        # terminated_by={"DEFINITE_POSITIVE_EXISTENCE"}
    ),
    ConTextRule(
        "risk",
        "UNCERTAIN",
        "BACKWARD",
        max_scope=1,
        pattern=[{"LOWER": {"IN": ["risk", "risks"]}}],
    ),
    ConTextRule(
        "risk factors for",
        "UNCERTAIN",
        "FORWARD",
        max_scope=5,
        pattern=[{"LOWER": "risk"}, {"LEMMA": "factor"}, {"LOWER": "for"}],
    ),
    ConTextRule("investigation of", "UNCERTAIN", "FORWARD", max_scope=1),
    ConTextRule("to exclude", "UNCERTAIN", "FORWARD",),
    ConTextRule("awaiting", "UNCERTAIN", "BIDIRECTIONAL", max_scope=2),
    ConTextRule("question of", "UNCERTAIN", "FORWARD", max_scope=4),
    ConTextRule("differential diagnosis:", "UNCERTAIN", "FORWARD", max_scope=4),
    ConTextRule("ddx:", "UNCERTAIN", "FORWARD", max_scope=4),
    ConTextRule(
        "currently being ruled out or has tested positive for",
        "UNCERTAIN",
        "BIDIRECTIONAL",
    ),
    ConTextRule(
        "person of interest",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        pattern=[
            {"LEMMA": {"IN": ["person", "patient"]}},
            {"LOWER": "of"},
            {"LOWER": "interest"},
        ],
    ),
    ConTextRule("under investigation", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextRule(
        "may be positive for",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[
            {"LOWER": {"IN": ["may", "might"]}},
            {"LOWER": "be"},
            {"LOWER": "positive"},
            {"LOWER": "for"},
        ],
    ),
    ConTextRule(
        "may be positive",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[
            {"LOWER": {"IN": ["may", "might"]}},
            {"LOWER": "be"},
            {"LOWER": "positive"},
        ],
    ),
    ConTextRule(
        "area with",
        "OTHER_EXPERIENCER",
        pattern=[
            {"LOWER": {"IN": ["area", "county", "comsmunity", "city"]}},
            {"LOWER": {"IN": ["with", "of"]}},
        ],
    ),
    ConTextRule(
        "facility with",
        "OTHER_EXPERIENCER",
        "FORWARD",
        pattern=[
            {"LOWER": "facility"},
            {"LOWER": {"IN": ["with", "has"]}},
            {"LOWER": "a"},
        ],
    ),
    ConTextRule("known to have", "OTHER_EXPERIENCER", "FORWARD"),
    ConTextRule(
        "same room",
        "OTHER_EXPERIENCER",
        pattern=[{"LOWER": "same"}, {"OP": "?"}, {"LOWER": {"REGEX": "room"}}],
    ),
    ConTextRule("in the building", "OTHER_EXPERIENCER", "BIDIRECTIONAL"),
    ConTextRule(
        "several residents",
        "OTHER_EXPERIENCER",
        "FORWARD",
        pattern=[{"LOWER": {"IN": ["multiple", "several"]}}, {"LOWER": "residents"}],
    ),
    ConTextRule(
        "one of the residents",
        "OTHER_EXPERIENCER",
        "FORWARD",
        pattern=[
            {"LOWER": {"IN": ["multiple", "several", "one"]}},
            {"LOWER": "of"},
            {"LOWER": "the"},
            {"LOWER": "residents"},
        ],
    ),
    ConTextRule("patients with", "OTHER_EXPERIENCER", "FORWARD",),
    ConTextRule(
        "travel",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["flew", "traveled", "travelled"]}}],
    ),
    ConTextRule("got back from", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextRule("was recently in", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextRule(
        "positive screen",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "positive criteria",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "positive triage",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "pending",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^test"}, "OP": "?"}, {"LOWER": "pending"}],
    ),
    ConTextRule(
        "screen positive",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "screen"}},
            {"OP": "?"},
            {"OP": "?"},
            {"LOWER": {"IN": ["positive", "pos"]}},
        ],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "possible",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "possibly",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "possible positive",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "possibl"}}, {"LOWER": "positive"}],
    ),
    ConTextRule(
        "risk of",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextRule(
        "likely",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextRule(
        "probable",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextRule(
        "probably",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextRule(
        "questionnaire",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=2,
    ),
    ConTextRule(
        "suspicion",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "suspect",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^suspect"}}],
    ),
    ConTextRule(
        "suspicious for",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule("differential diagnosis", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextRule(
        "differential diagnosis",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        pattern=[{"LOWER": "ddx"}, {"LOWER": ":", "OP": "?"}],
    ),
    ConTextRule("symptoms", "SYMPTOM", max_scope=4,),
    ConTextRule(
        "symptoms of",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19"},
        pattern=[
            {"LOWER": "positive", "OP": "?"},
            {"LEMMA": {"IN": ["sign", "symptom"]}},
            {"LOWER": "of"},
        ],
        max_scope=4,
    ),
    ConTextRule(
        "s/s", "UNCERTAIN", "BIDIRECTIONAL", allowed_types={"COVID-19"}, max_scope=5
    ),
    ConTextRule(
        "sx", "UNCERTAIN", "BIDIRECTIONAL", allowed_types={"COVID-19"}, max_scope=5
    ),
    ConTextRule(
        "potential",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^potential"}}],
    ),
    ConTextRule(
        "possible exposure",
        "UNCERTAIN",
        "BIDIRECTIONAL",  # allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[
            {"LOWER": {"IN": ["possible", "potential"]}},
            {"OP": "?"},
            {"LOWER": "exposure"},
        ],
    ),
    ConTextRule(
        "exposure",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^exposure"}}],
        on_match=callbacks.disambiguate_exposure,
    ),
    ConTextRule(
        "may have been exposed",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "exposed to <X>",
        "CONTACT",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[
            {"LOWER": {"REGEX": "^expos"}},
            {"LOWER": "to"},
            {"POS": "NOUN", "OP": "?", "_": {"concept_tag": ""}},
        ],
    ),
    ConTextRule(
        "concern for",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"IN": ["concern"]}}, {"LOWER": {"IN": ["of", "for"]}}],
    ),
    ConTextRule("concerns", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextRule("if positive", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextRule("if negative", "UNCERTAIN", "BIDIRECTIONAL"),
    # ConTextRule("if", "UNCERTAIN", "BIDIRECTIONAL", max_scope=5), # "if his covid-19 is positive"
    ConTextRule("if you", "FUTURE/HYPOTHETICAL", "FORWARD"),
    ConTextRule(
        "c/f", "UNCERTAIN", "FORWARD", allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "assessed for",
        "UNCERTAIN",
        "FORWARD",
        pattern=[{"LOWER": {"IN": ["assess", "assessed"]}}, {"LOWER": "for"}],
    ),
    ConTextRule("concerning for", "UNCERTAIN", direction="FORWARD"),
    ConTextRule("r/o", "UNCERTAIN", direction="BIDIRECTIONAL", max_scope=2,),
    ConTextRule("r/o.", "UNCERTAIN", direction="BIDIRECTIONAL", max_scope=2,),
    ConTextRule(
        "rule out",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
        pattern=[{"LEMMA": "rule"}, {"TEXT": "-", "OP": "?"}, {"LOWER": "out"}],
    ),
    ConTextRule(
        "ro",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=2,
    ),
    ConTextRule(
        "be ruled out",
        "UNCERTAIN",
        "FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"IN": ["be", "being"]}},
            {"LOWER": "ruled"},
            {"LOWER": "out"},
            {"LOWER": "for"},
        ],
    ),
    ConTextRule(
        "vs.",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
        pattern=[{"LOWER": {"REGEX": "^(vs\.?|versus)$"}}],
    ),
    # certainty = low
    ConTextRule("unlikely", "UNLIKELY", "BIDIRECTIONAL"),
    ConTextRule("unlikely to be", "UNLIKELY", "FORWARD"),
    ConTextRule(
        "doubt", "UNLIKELY", "FORWARD", allowed_types={"COVID-19", "OTHER_CORONAVIRUS"}
    ),
    ConTextRule(
        "doubtful",
        "UNLIKELY",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "unlikely to be positive",
        "UNLIKELY",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule("low suspicion", "UNLIKELY", "BIDIRECTIONAL"),
    ConTextRule("low probability", "UNLIKELY", "BIDIRECTIONAL"),
    ConTextRule(
        "not recommend",
        "UNLIKELY",
        "FORWARD",
        pattern=[
            {"LOWER": "not"},
            {"LOWER": "recommend"},
            {"LOWER": {"REGEX": "test"}},
        ],
    ),
    ConTextRule("extremely low", "UNLIKELY", "BACKWARD", max_scope=3),
    ConTextRule("low risk of", "UNLIKELY", "FORWARD", max_scope=3),
    ConTextRule("is unlikely", "UNLIKELY", "BACKWARD"),
    ConTextRule(
        "low risk of",
        "UNLIKELY",
        "FORWARD",
        pattern=[{"LOWER": "low"}, {"LOWER": "risk"}, {"LOWER": {"IN": ["in", "for"]}}],
    ),
    ConTextRule(
        "positive patients",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["pos", "positive", "+"]}},
            {"LOWER": {"IN": ["pts", "patients"]}},
        ],
    ),
    ConTextRule(
        "patients",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        max_scope=10,
        pattern=[{"LOWER": {"IN": ["pts", "patients"]}}],
    ),
    ConTextRule(
        "other person",
        "OTHER_EXPERIENCER",
        "FORWARD",
        pattern=[{"_": {"concept_tag": "other_experiencer"}, "OP": "+"},],
    ),
    ConTextRule(
        "family member",
        "OTHER_EXPERIENCER",
        "FORWARD",
        pattern=[{"_": {"concept_tag": "family"}, "OP": "+"},],
        on_match=callbacks.family_speaker,
    ),
    ConTextRule(
        "<OTHER_EXPERIENCER> tested positive",
        "OTHER_EXPERIENCER",
        pattern=[
            {"_": {"concept_tag": {"IN": ["other_experiencer", "family"]}}, "OP": "+"},
            {"LOWER": {"REGEX": "^test"}},
            {"_": {"concept_tag": "positive"}, "OP": "+"},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextRule(
        "other patient",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "other"}},
            {"LOWER": {"REGEX": "(patient|resident|veteran|soldier)"}},
        ],
    ),
    ConTextRule(
        "a patient",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": "a"},
            {"LOWER": {"IN": ["patient", "pt", "pt.", "resident"]}},
        ],
    ),
    ConTextRule("any one", "OTHER_EXPERIENCER", "BIDIRECTIONAL", max_scope=100),
    ConTextRule(
        "contact with",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        max_scope=1000,
        pattern=[
            {"LEMMA": "contact", "POS": {"NOT_IN": ["VERB"]}},
            {"LOWER": "with"},
            {"LOWER": "known", "OP": "?"},
        ],
    ),
    ConTextRule("had contact", "OTHER_EXPERIENCER", "BIDIRECTIONAL", max_scope=1000,),
    ConTextRule("same building", "OTHER_EXPERIENCER", "BIDIRECTIONAL", max_scope=1000,),
    ConTextRule("same floor", "OTHER_EXPERIENCER", "BIDIRECTIONAL", max_scope=1000,),
    ConTextRule(
        "cared for",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",  # The patient is a nurse who cared for a patient with COVID-19
        pattern=[{"LEMMA": "care"}, {"LOWER": "for"}],
    ),
    ConTextRule(
        "the woman/man",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["a", "the"]}},
            {"LOWER": {"IN": ["man", "men", "woman", "women"]}},
        ],
    ),
    ConTextRule(
        "XXmate",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",  # "roommate", "housemate", etc...
        pattern=[{"LOWER": {"REGEX": "mates?$"}}],
    ),
    ConTextRule(
        "clean",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[{"LEMMA": "clean", "POS": "VERB"}],
    ),  # "She has been cleaning covid-19 positive rooms"
    ConTextRule(
        "A X tested positive",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["a", "an", "another"]}},
            {"POS": "NOUN"},
            {"LOWER": "tested"},
            {"LOWER": "positive"},
        ],
    ),
    # Since this is not very clinical, more likely to be from the pt's perspective; should review
    # Example: " is concerned about the coronavirus as she works at costco
    # ConTextRule("request", "FUTURE/HYPOTHETICAL", "FORWARD", pattern=[{"LEMMA": "request"}]),
    ConTextRule(
        "concerned about",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        pattern=[{"LOWER": {"REGEX": "concern"}}, {"LOWER": "about"}],
        max_scope=3,
    ),
    ConTextRule(
        "patient concern for",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[
            {"LOWER": {"IN": ["pt", "patient"]}},
            {"LOWER": {"IN": ["concern"]}},
            {"LOWER": {"IN": ["of", "for"]}},
        ],
    ),
    ConTextRule(
        "he thinks he has",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        pattern=[
            {"LOWER": {"IN": ["he", "she"]}},
            {"LOWER": {"REGEX": "(think|thought)"}},
            {"LOWER": {"IN": ["he", "she"]}},
            {"LOWER": {"IN": ["has", "had", "have"]}},
        ],
    ),
    ConTextRule(
        "she would like",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        pattern=[{"POS": "PRON"}, {"LOWER": "would"}, {"LOWER": "like"}],
    ),
    ConTextRule(
        "desires", "FUTURE/HYPOTHETICAL", "FORWARD", pattern=[{"LEMMA": "desire"}]
    ),
    ConTextRule(
        "concerned for",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        pattern=[{"LOWER": "concerned"}, {"LOWER": "for"}],
    ),
    ConTextRule(
        "prepare for",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "prepare"}},
            {"LOWER": {"IN": ["for", "against"]}},
        ],
    ),
    ConTextRule("mers", "NOT_RELEVANT", "FORWARD", allowed_types={"COVID-19"}),
    ConTextRule(
        "seen in", "NOT_RELEVANT", "FORWARD", allowed_types={"COVID-19"}, max_scope=2
    ),  # "commonly seen in COVID-19 pneumonia"
    ConTextRule(
        "seen in the setting of",
        "NOT_RELEVANT",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
        pattern=[
            {"LOWER": "seen"},
            {"LOWER": "in"},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": "setting"},
            {"LOWER": "of"},
        ],
    ),
    # These mental health terms below will rule out cases where the patient
    # is anxious about the pandemic or about being exposed to COVID-19
    # but may not have any symptoms or diagnosis.
    # Example: "The patient is very anxious about the COVID-19 disease and is scared they will catch it."
    # But you should be cautious about them as well because they could cause potential false negatives.
    ConTextRule(
        "anxiety",
        "MENTAL_HEALTH",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        pattern=[
            {
                "LOWER": {
                    "IN": [
                        "anxious",
                        "anxiety",
                        "afraid",
                        "fear",
                        "fears",
                        "nervous",
                        "scared",
                        "scare",
                        "panic",
                        "panick",
                        "panicking",
                        "obsess",
                        "obsessed",
                        "obsessing",
                        "stress",
                        "stressor",
                        "stressors",
                    ]
                }
            }
        ],
        max_scope=5,
    ),
    # Cancel vacation due to COVID
    ConTextRule(
        "cancel vacation",
        "FUTURE/HYPOTHETICAL",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^cancel"}},
            {
                "LOWER": {
                    "IN": [
                        "flight",
                        "flights",
                        "plan",
                        "plans",
                        "trip",
                        "trips",
                        "vacation",
                    ]
                },
            },
        ],
    ),
    ConTextRule(
        "supposed to travel",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": "supposed"},
            {"LOWER": "to"},
            {"LOWER": {"IN": ["travel", "go", "visit"]}},
        ],
    ),
    ConTextRule("called off", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL"),
    ConTextRule("goals:", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule(
        "a positive case of",
        "NOT_RELEVANT",
        "FORWARD",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "a confirmed case of",
        "NOT_RELEVANT",
        "FORWARD",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "there has been",
        "NOT_RELEVANT",
        "FORWARD",
        allowed_types={"COVID-19"},
        max_scope=10,  # "He was in NYC, where there have been manyt confirmed cases"
        pattern=[
            {"LOWER": "there"},
            {"LOWER": {"IN": ["has", "have"]}},
            {"LOWER": "been"},
        ],
    ),
    ConTextRule(
        "in the area",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": "in"},
            {"LOWER": "the"},
            {"LOWER": {"IN": ["area", "community"]}},
        ],
    ),
    ConTextRule(
        "cases",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "outbreak of",
        "NOT_RELEVANT",
        "FORWARD",
        allowed_types={"COVID-19"},
        max_scope=1,
    ),
    ConTextRule(
        "outbreak",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "epidemic",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "pandemic",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "national emergency",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "crisis",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "situation",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "mandate",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
        pattern=[{"LOWER": {"REGEX": "mandate"}}],
    ),
    ConTextRule(
        "news",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        pattern=[
            {
                "LOWER": {
                    "IN": [
                        "news",
                        "media",
                        "tv",
                        "television",
                        "broadcast",
                        "headline",
                        "headlines",
                        "newspaper",
                        "newspapers",
                    ]
                }
            }
        ],
    ),
    ConTextRule("clinic cancellation", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # ConTextRule("flight/trip", "NOT_RELEVANT", "BIDIRECTIONAL", allowed_types={"COVID-19"},
    #             pattern=[{"LOWER": {"IN": ["flight", "flights",
    #                                        "trip", "trips",
    #                                 "vacation", "vacations"]}}]), # "cancelled his flight because of coronavirus"
    ConTextRule(
        "read about",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        pattern=[{"LOWER": {"REGEX": "^read"}}, {"LOWER": "about"}],
    ),
    ConTextRule(
        "deployment",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "deploy"}}],
        allowed_types={"COVID-19"},
    ),
    # ConTextRule("current events", "NOT_RELEVANT", "BIDIRECTIONAL",
    #             pattern=[{"LOWER": {"IN": ["current", "recent"]}},
    #                      {"LOWER": {"REGEX": "^event"}}]), # Discussing current events for cognitive understanding
    # ConTextRule("topics", "NOT_RELEVANT", "BIDIRECTIONAL",
    #             pattern=[{"LOWER": {"REGEX": "^topic"}}]), # Discussing current events for cognitive understanding
    ConTextRule(
        "come in close contact",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",  # Common phrase used in screenings
        allowed_types={"COVID-19", "travel"},
        pattern=[
            {"LOWER": {"IN": ["come", "been"]}},
            {"LOWER": "in"},
            {"LOWER": "close"},
            {"LOWER": "contact"},
            {"LOWER": "with"},
        ],
    ),
    ConTextRule("?", "NOT_RELEVANT", "BACKWARD", max_scope=2),
    # ConTextRule("in the last 14 days", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextRule("have you had close contact", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # 'Checkup done via telephone because of COVID-19.'
    # Won't match: 'Pt notified via telephone of his positive COVID-19 result.'
    # ConTextRule("telephone", "NOT_RELEVANT", "BIDIRECTIONAL", pattern=[{"LOWER": {"IN": ["telephone", "telehealth"]}}],
    #             on_match=callbacks.check_telephone_notification),
    ConTextRule("the group", "NOT_RELEVANT", "FORWARD"),  # Group therapy sessions
    ConTextRule(
        "session", "NOT_RELEVANT", "FORWARD", pattern=[{"LOWER": {"REGEX": "^session"}}]
    ),  # Group therapy sessions
    # ConTextRule("mental health", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextRule("website", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextRule("web site", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextRule("internet", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # ConTextRule("global", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextRule("worldwide", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextRule("world wide", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextRule("world-wide", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # "Patients with confirmed covid-19 should stay home"
    ConTextRule(
        "patients with",
        "NOT_RELEVANT",
        "FORWARD",
        max_scope=3,
        pattern=[
            {"LOWER": {"IN": ["persons", "patients", "people"]}},
            {"LOWER": "with"},
            {"LOWER": "confirmed"},
            {"LOWER": "or", "OP": "?"},
            {"LOWER": "suspected", "OP": "?"},
        ],
    ),
    ConTextRule(
        "nurse notes:",
        "NOT_RELEVANT",
        "FORWARD",  # often precedes a screening
        pattern=[{"LOWER": {"IN": ["nurse", "nurses", "rn"]}}, {"LOWER": "notes"}],
    ),
    # ConTextRule("mental health", "NOT_RELEVANT", "BIDIRECTIONAL",
    #             pattern=[{"LOWER": {"IN": ["psychiatry", "psychotic", "paranoid", "paranoia", "psych"]}}]),
    ConTextRule("countries with cases", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # ConTextRule(":", "NOT_RELEVANT", "BACKWARD", max_scope=1), # "Coronavirus: ..."
    ConTextRule(
        "cases of", "NOT_RELEVANT", "FORWARD", max_scope=3
    ),  # "his daughter lives in Seoul, where cases of coronavirus have been discovered"
    # ConTextRule("alert and oriented", "NOT_RELEVANT", "FORWARD"),
    # ConTextRule("the", "NOT_RELEVANT", "FORWARD", max_scope=1, allowed_types={"COVID-19"}), # When clinicians are relaying a patient's anxieties or questions, they often use 'the coronavirus', whereas when they're using their own clinical judgment they just say 'coronavirus'
    ConTextRule(
        "been in contact with anyone confirmed", "NOT_RELEVANT", "BIDIRECTIONAL"
    ),
    ConTextRule(
        "error", "NOT_RELEVANT", "BIDIRECTIONAL"
    ),  # "COVID-19 marked positive in error"
    ConTextRule(
        "elective", "NOT_RELEVANT", "BIDIRECTIONAL", max_scope=5
    ),  # "elective surgeries will be scheduled after COVID-19 has ended"
    ConTextRule(
        "rescheduled",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        pattern=[{"LEMMA": "reschedule"}],
    ),
    ConTextRule(
        "postponed", "NOT_RELEVANT", "BIDIRECTIONAL", pattern=[{"LEMMA": "postpone"}]
    ),
    ConTextRule(
        "barriers to travel",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        pattern=[{"LEMMA": "barrier"}, {"LOWER": "to"}, {"LOWER": "travel"}],
    ),
    # Contact with sick individuals
    ConTextRule(
        "positive individual",
        "CONTACT",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["positive", "+", "confirmed"]}, "POS": "ADJ"},
            {"LEMMA": {"IN": ["individual", "contact", "patient"]}},
        ],
    ),
    ConTextRule(
        "someone who has tested positive",
        "CONTACT",
        "BIDIRECTIONAL",
        pattern=[
            {"LEMMA": {"IN": ["someone", "person", "people"]}},
            {"LOWER": "who"},
            {"LEMMA": {"IN": ["has", "have"]}},
            {"LOWER": "tested"},
            {"LOWER": "positive"},
        ],
    ),
    ConTextRule(
        "contact with",
        "CONTACT",
        "FORWARD",
        pattern=[{"LOWER": "contact"}, {"LOWER": {"REGEX": "w(/|ith)?$"}}],
    ),
    ConTextRule("social worker", "IGNORE", "BIDIRECTIONAL"),
    ConTextRule("initially negative", "IGNORE", "BIDIRECTIONAL"),
    ConTextRule("likely recovered", "IGNORE", "BIDIRECTIONAL"),
    ConTextRule("not aware", "IGNORE", "BIDIRECTIONAL"),
    ConTextRule("positive cases", "IGNORE", "BIDIRECTIONAL"),
    ConTextRule("client history", "IGNORE", "BIDIRECTIONAL"),
    ConTextRule("emergency contact", "IGNORE", "BIDIRECTIONAL"),
    ConTextRule("several positive", "IGNORE", "BIDIRECTIONAL"),
    ConTextRule("special instructions:", "IGNORE", "BIDIRECTIONAL"),
    ConTextRule(
        "positive symptoms",
        "IGNORE",
        "BIDIRECTIONAL",
        pattern=[{"LOWER": "positive"}, {"LOWER": {"REGEX": "symptom|sign"}}],
    ),
    # Ignore "history" in "history of present illness"
    ConTextRule(
        "history of present illness", "IGNORE", "TERMINATE", allowed_types={"COVID-19"}
    ),
    ConTextRule("does not know", "IGNORE", "TERMINATE"),
    ConTextRule(
        "benign", "SPECIFIED_STRAIN", "BIDIRECTIONAL", allowed_types={"COVID-19"}
    ),
    ConTextRule("but", "CONJ", "TERMINATE"),
    ConTextRule("therefore", "CONJ", "TERMINATE"),
    ConTextRule(";", "CONJ", "TERMINATE"),
    # "Positive for X" should terminate
    ConTextRule("Metapneumovirus", "CONJ", "TERMINATE"),
    ConTextRule(
        "flu", "CONJ", "TERMINATE", pattern=[{"LOWER": {"REGEX": "flu"}}]
    ),  # Stop modifiers for flu
    # ConTextRule("who", "CONJ", "TERMINATE"), # example: "male with history of afib, who recently came back from China"
]
