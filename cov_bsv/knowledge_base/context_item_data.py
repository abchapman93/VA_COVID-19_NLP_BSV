from medspacy.context import ConTextItem
from . import callbacks

context_item_data = [
    # "NEGATED_EXISTENCE" will be used to negate entities
    # ie., "COVID-19 not detected"
    ConTextItem(
        literal="Not Detected",
        category="NEGATED_EXISTENCE",
        rule="BACKWARD",
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
    ConTextItem(
        ": negative",
        "NEGATED_EXISTENCE",
        rule="BACKWARD",
        max_scope=3,  # Set a small window, but allow for whitespaces
        max_targets=1,
    ),
    ConTextItem("not been detected", "NEGATED_EXISTENCE", rule="BACKWARD"),
    ConTextItem("none detected", "NEGATED_EXISTENCE", rule="BACKWARD"),
    ConTextItem("free from", "NEGATED_EXISTENCE", rule="FORWARD"),
    ConTextItem(
        "not tested",
        "NEGATED_EXISTENCE",
        rule="BACKWARD",
        pattern=[{"LOWER": "not"}, {"LOWER": "been", "OP": "?"}, {"LOWER": "tested"}],
    ),
    ConTextItem(
        "Ref Not Detected",
        "IGNORE",
        rule="TERMINATE",
        pattern=[
            {"LOWER": "ref"},
            {"LOWER": ":"},
            {"LOWER": "not"},
            {"LOWER": "detected"},
        ],
        max_targets=1,
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "not indicated", "NEGATED_EXISTENCE", rule="BACKWARD", max_scope=5
    ),
    ConTextItem(
        "NEGATIVE NEG",
        "NEGATED_EXISTENCE",
        rule="BACKWARD",  # Lab results
        pattern=[{"TEXT": "NEGATIVE"}, {"IS_SPACE": True, "OP": "*"}, {"TEXT": "NEG"}],
        max_scope=1,
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "negative screen",
        "NEGATED_EXISTENCE",
        rule="BIDIRECTIONAL",
        max_scope=2,
    ),
    ConTextItem(
        "negative test", "NEGATED_EXISTENCE", rule="BIDIRECTIONAL", max_scope=4
    ),
    ConTextItem(
        "without any", "NEGATED_EXISTENCE", rule="FORWARD", max_scope=2
    ),
    ConTextItem("denies", "NEGATED_EXISTENCE", rule="FORWARD", max_scope=10),
    ConTextItem(
        "denies any", "NEGATED_EXISTENCE", rule="FORWARD", max_scope=10
    ),
    ConTextItem(
        "denies travel", "NEGATED_EXISTENCE", rule="FORWARD", max_scope=10
    ),
    ConTextItem("denied", "NEGATED_EXISTENCE", rule="FORWARD", max_scope=10),
    ConTextItem("no evidence", "NEGATED_EXISTENCE", rule="FORWARD"),
    ConTextItem(
        "history of",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        max_scope=4,
        pattern=[
            {"LOWER": "no"},
            {"LOWER": {"IN": ["hx", "-hx", "history"]}},
            {"LOWER": "of"},
        ],
    ),
    ConTextItem(
        "no diagnosis of",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"OP": "?"},
            {"LOWER": {"IN": ["dx", "diagnosis"]}},
            {"LOWER": "of", "OP": "?"},
        ],
    ),
    ConTextItem(
        "no", "NEGATED_EXISTENCE", rule="FORWARD", max_scope=2
    ),  # Limit to a small scope
    ConTextItem("no positive", "NEGATED_EXISTENCE", rule="FORWARD"),
    ConTextItem("no one", "NEGATED_EXISTENCE", rule="FORWARD"),
    ConTextItem("no residents", "NEGATED_EXISTENCE", rule="FORWARD"),
    ConTextItem(
        "no confirmed cases",
        "NEGATED_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": "no"}, {"LOWER": "confirmed"}, {"LEMMA": "case"}],
    ),
    ConTextItem(
        "not been confirmed",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        max_scope=2,
        pattern=[
            {"LOWER": {"IN": ["not", "n't"]}},
            {"LOWER": "been", "OP": "?"},
            {"LOWER": "confirmed"},
        ],
    ),
    ConTextItem("no known", "NEGATED_EXISTENCE", rule="FORWARD", max_scope=5),
    ConTextItem(
        "no contact with",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        max_scope=None,
        pattern=[
            {"LOWER": "no"},
            {"OP": "?"},
            {"LOWER": "contact"},
            {"LOWER": {"REGEX": "w/?(ith)?$"}, "OP": "?"},
        ],
    ),
    ConTextItem(
        "answer no",
        "NEGATED_EXISTENCE",
        rule="BIDIRECTIONAL",  # "Veteran answered no to being exposed to coronavirus"
        pattern=[
            {"LOWER": {"REGEX": "^answer"}},
            {"TEXT": '"', "OP": "?"},
            {"LOWER": {"IN": ["no", "negative", "neg"]}},
            {"TEXT": '"', "OP": "?"},
        ],
    ),
    ConTextItem("negative", "NEGATED_EXISTENCE", rule="BIDIRECTIONAL",),
    ConTextItem(
        "negative for",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": {"IN": ["negative", "neg"]}}, {"LOWER": "for"}],
    ),
    # ConTextItem("is negative for", "NEGATED_EXISTENCE", rule="FORWARD"),
    ConTextItem("not positive", "NEGATED_EXISTENCE", rule="BIDIRECTIONAL"),
    ConTextItem(
        "excluded", "NEGATED_EXISTENCE", rule="BIDIRECTIONAL", max_scope=4
    ),
    ConTextItem(
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
    ConTextItem(
        "negative screening for",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": "negative"},
            {"LOWER": {"REGEX": "screen"}},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextItem(
        "screening negative",
        "NEGATED_EXISTENCE",
        rule="BACKWARD",
        pattern=[{"LOWER": {"REGEX": "^screen"}}, {"LOWER": {"REGEX": "^neg"}}],
    ),
    ConTextItem(
        "screened negative for",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "^screen"}},
            {"LOWER": {"REGEX": "^neg"}},
            {"LOWER": "for"},
        ],
    ),
    ConTextItem("does not screen positive", "NEGATED_EXISTENCE"),
    ConTextItem(
        "is negative",
        "NEGATED_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[{"LEMMA": "be"}, {"LOWER": "negative"}],
    ),
    ConTextItem(
        "not test positive", "NEGATED_EXISTENCE", rule="BIDIRECTIONAL"
    ),
    ConTextItem(
        "no screening for",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "not?"}},
            {"LOWER": {"REGEX": "^screen"}},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextItem("no signs of", "NEGATED_EXISTENCE", rule="FORWARD"),
    ConTextItem(
        "no symptoms",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": "no"}, {"LOWER": {"REGEX": "(sign|symptom)"}}],
    ),
    ConTextItem(
        "no testing for",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "^no"}},
            {"LOWER": {"REGEX": "^test"}},
            {"LOWER": "for"},
        ],
    ),
    ConTextItem(
        "no indication of",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"LOWER": {"REGEX": "indication"}},
            {"LOWER": {"IN": ["of", "for"]}, "OP": "?"},
        ],
    ),
    ConTextItem(
        "no exposure",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": "no"}, {"LOWER": {"REGEX": "^exposure"}}],
    ),
    ConTextItem(
        "without signs/symptoms",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": "without"},
            {"OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms"]}},
            {"LOWER": "or", "OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms"]}, "OP": "?"},
        ],
    ),
    ConTextItem(
        "w/o signs/symptoms",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": "w/o"},
            {"OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms"]}},
            {"LOWER": "or", "OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms"]}, "OP": "?"},
        ],
    ),
    ConTextItem(
        "does not have any signs/symptoms",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19"},
        pattern=[
            {"LOWER": "does"},
            {"LOWER": {"IN": ["not", "n't"]}},
            {"LOWER": "have"},
            {"LOWER": "any", "OP": "?"},
            {"LOWER": {"IN": ["signs", "symptoms", "ss", "s/s"]}},
        ],
    ),
    ConTextItem("not have", "NEGATED_EXISTENCE", max_scope=5),
    ConTextItem(
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
    ConTextItem("no evidence of", "NEGATED_EXISTENCE", rule="FORWARD"),
    ConTextItem(
        "does not meet criteria", "NEGATED_EXISTENCE", rule="BIDIRECTIONAL"
    ),
    ConTextItem(
        "no concern for",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"LOWER": "concern"},
            {"LOWER": {"IN": ["for", "of"]}},
        ],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "not at risk",
        "NEGATED_EXISTENCE",
        "FORWARD",
        pattern=[{"LOWER": "not"}, {"LOWER": "at"}, {"LOWER": "risk"}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "no risk",
        "NEGATED_EXISTENCE",
        "FORWARD",
        pattern=[{"LOWER": "no"}, {"OP": "?"}, {"LOWER": "risk"}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "no suspicion",
        "NEGATED_EXISTENCE",
        "FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"LOWER": {"REGEX": "^suspicion"}},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextItem("not suspect", "NEGATED_EXISTENCE", rule="FORWARD"),
    ConTextItem("not", "NEGATED_EXISTENCE", rule="FORWARD", max_scope=4),
    ConTextItem(
        "ruled out for",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "is ruled out",
        "NEGATED_EXISTENCE",
        rule="BACKWARD",
        pattern=[
            {"LOWER": {"IN": ["is", "are", "were"]}},
            {"OP": "?", "POS": "ADV"},
            {"LOWER": "ruled"},
            {"LOWER": "out"},
        ],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "does not meet criteria",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "is not likely",
        "NEGATED_EXISTENCE",
        rule="BACKWARD",
        pattern=[
            {"LOWER": {"IN": ["is", "are"]}},
            {"LOWER": "not"},
            {"LOWER": "likely"},
        ],
    ),
    ConTextItem(
        "no travel",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": "no"}, {"LOWER": "recent", "OP": "?"}, {"LOWER": "travel"}],
    ),
    ConTextItem(
        "not be in",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        allowed_types={"location", "COVID-19"},
    ),
    ConTextItem(
        "cleared from",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "^clear"}},
            {"LOWER": {"IN": ["of", "for", "from"]}},
        ],
    ),
    ConTextItem(
        "no history of travel",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": "no"},
            {"LOWER": {"IN": ["hx", "history"]}},
            {"LOWER": "of", "OP": "?"},
            {"LOWER": "travel"},
        ],
        allowed_types={"location", "COVID-19"},
    ),
    ConTextItem(
        "no exposure to",
        "NEGATED_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": "no"}, {"OP": "?"}, {"LOWER": "exposure"}, {"LOWER": "to"}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "no contact with",
        "NEGATED_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": "no"}, {"OP": "?"}, {"LEMMA": "contact"}, {"LOWER": "with"}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "not have contact with",
        "NEGATED_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LOWER": "not"},
            {"LOWER": "have"},
            {"OP": "?"},
            {"LOWER": "contact"},
            {"LOWER": "with"},
        ],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "no X contacts",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"IN": ["no", "any"]}},
            {"LOWER": "known", "OP": "?"},
            {"OP": "?"},
            {"LEMMA": "contact"},
            {"LOWER": "with", "OP": "?"},
        ],
    ),
    ConTextItem(
        "anyone with", "NEGATED_EXISTENCE", rule="FORWARD", max_scope=None
    ),
    ConTextItem(
        "no symptoms of",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19"},
    ),
    ConTextItem(
        "no risk factors",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19"},
    ),
    ConTextItem(
        "no confirmed cases",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19"},
    ),
    ConTextItem(
        "does not meet screening criteria",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
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
    ConTextItem(": no", "NEGATED_EXISTENCE", rule="BACKWARD", max_scope=4),
    ConTextItem(
        "no report",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": "no"}, {"LOWER": {"REGEX": "report"}}],
    ),
    ConTextItem(
        "not diagnosed with",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        max_scope=2,
        pattern=[
            {"LOWER": {"IN": ["not", "never"]}},
            {"OP": "?"},
            {"LOWER": "diagnosed"},
            {"LOWER": "with"},
        ],
    ),
    ConTextItem(
        "not been tested or diagnosed with",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        max_scope=2,
    ),
    ConTextItem(
        "not been tested for or diagnosed with",
        "NEGATED_EXISTENCE",
        rule="FORWARD",
        max_scope=2,
    ),
    ConTextItem(
        "not tested positive for",
        "NEGATED_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LOWER": "not"},
            {"LOWER": {"REGEX": "^test"}},
            {"_": {"concept_tag": "positive"}, "OP": "+"},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextItem("not tested", "NEGATED_EXISTENCE", rule="FORWARD",),
    ConTextItem(
        "not tested or diagnosed", "NEGATED_EXISTENCE", rule="FORWARD",
    ),

    # "DEFINITE_POSITIVE_EXISTENCE" will be used to set is_positive to True
    ConTextItem(
        "confirmed",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BIDIRECTIONAL",
        on_match=callbacks.disambiguate_confirmed,
        max_scope=2,  # Too ambiguous of a word, needs to be very close
    ),
    ConTextItem("known", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=2),
    ConTextItem(
        "positive for",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": {"IN": ["pos", "positive", "+"]}}, {"LOWER": "for"}],
    ),
    ConTextItem(
        "positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BIDIRECTIONAL",
        on_match=callbacks.disambiguate_positive,
    ),
    ConTextItem(
        "pos status", "DEFINITE_POSITIVE_EXISTENCE", rule="BACKWARD", max_scope=3
    ),
    ConTextItem(
        "results are positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BACKWARD",
        max_scope=3,
        pattern=[
            {"LOWER": {"REGEX": "result"}},
            {"LOWER": {"IN": ["is", "are"]}},
            {"LOWER": "positive"},
        ],
    ),
    ConTextItem(
        "pos", "DEFINITE_POSITIVE_EXISTENCE", rule="BIDIRECTIONAL", max_scope=5
    ),
    ConTextItem(
        "results pos", "DEFINITE_POSITIVE_EXISTENCE", rule="BIDIRECTIONAL", max_scope=5
    ),
    ConTextItem("positivity", "DEFINITE_POSITIVE_EXISTENCE", rule="BACKWARD"),
    ConTextItem(
        "test +",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^test"}},
            {"LOWER": {"IN": ["positive", "pos", "+", "(+)"]}},
        ],
    ),
    ConTextItem("+ve", "DEFINITE_POSITIVE_EXISTENCE", rule="BIDIRECTIONAL",),
    ConTextItem(
        "(+)",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[{"TEXT": {"IN": ["(+)", "+"]}}],
        max_scope=1,
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS", "sign/symptom"},
    ),
    ConTextItem(
        "(+)",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[{"TEXT": {"IN": ["(+)", "+"]}}, {"LOWER": "for"}],
        max_scope=1,
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "test remains positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BACKWARD",
        pattern=[
            {"LOWER": {"IN": ["test", "pcr"]}},
            {"LOWER": "remains"},
            {"LOWER": {"IN": ["pos", "positive", "+", "(+)"]}},
        ],
    ),
    ConTextItem(
        "notified of positive results",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "notif(y|ied)"}},
            {"OP": "?"},
            {"LOWER": "of"},
            {"_": {"concept_tag": "positive"}, "OP": "+"},
            {"LOWER": {"REGEX": "results?|test(ing)?|status"}},
        ],
    ),
    ConTextItem(
        "notified the veteran of positive results",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "notif(y|ied)"}},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": {"IN": ["veteran", "patient", "family"]}},
            {"LOWER": "of"},
            {"_": {"concept_tag": "positive"}, "OP": "+"},
            {"LOWER": {"REGEX": "results?|test(ing)?|status"}},
        ],
    ),
    ConTextItem(
        "likely secondary to",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        max_scope=1,
    ),
    ConTextItem(
        "Problem:", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=10
    ),
    ConTextItem(
        "PROBLEM LIST:", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=10
    ),
    ConTextItem(
        "current problems:", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=10
    ),
    ConTextItem(
        "Problem List of", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=10
    ),
    ConTextItem(
        "active problems:", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=10
    ),
    ConTextItem(
        "acute problems", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=10
    ),
    ConTextItem(
        "admission diagnosis:",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "admi(t|ssion)"}},
            {"LOWER": {"IN": ["diagnosis", "dx", "dx."]}},
            {"LOWER": ":", "OP": "?"},
        ],
    ),
    ConTextItem(
        "Reason for admission:",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        max_scope=4,
    ),
    ConTextItem(
        "treatment of", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=4
    ),
    ConTextItem(
        "Admitting Diagnosis:",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        max_scope=4,
        pattern=[
            {"LOWER": "admitting", "OP": "?"},
            {"LOWER": {"IN": ["diagnosis", "dx", "dx."]}},
        ],
    ),
    ConTextItem("dx:", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=4,),
    ConTextItem(
        "diagnosed <DATE>",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BACKWARD",
        max_scope=4,
        pattern=[
            {"LOWER": {"REGEX": "(diagnos|dx)(ed)?"}},
            {"LOWER": {"REGEX": "[\d]{1,2}/[\d]{1,2}"}},
        ],
    ),
    ConTextItem("Reason for admission:", "ADMISSION", rule="FORWARD", max_scope=6,),
    ConTextItem("inpatient with", "ADMISSION", rule="FORWARD", max_scope=6,),
    ConTextItem("discharged from", "ADMISSION", rule="FORWARD", max_scope=6,),
    ConTextItem(
        "diagnosed with", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=6,
    ),
    ConTextItem(
        "found to be positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BACKWARD",
        max_scope=6,
    ),
    ConTextItem(
        "found to be positive for",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        max_scope=6,
    ),
    ConTextItem("+ test", "DEFINITE_POSITIVE_EXISTENCE",),
    ConTextItem(
        "in icu for",
        "ADMISSION",
        rule="FORWARD",
        max_scope=6,
        pattern=[
            {"LOWER": "in"},
            {"LOWER": {"REGEX": "^m?icu"}},
            {"LOWER": {"IN": ["for", "with"]}},
        ],
    ),
    ConTextItem(
        "admitted <DATE>",
        "ADMISSION",
        rule="FORWARD",
        pattern=[
            {"LEMMA": "admit", "POS": "VERB"},
            {"LOWER": {"REGEX": "^[\d]{1,2}/[\d]{1,2}"}},
        ],
    ),
    ConTextItem(
        "admitted with",
        "ADMISSION",
        rule="FORWARD",
        max_scope=None,
        pattern=[
            {"LOWER": {"REGEX": "admit"}, "POS": "VERB"},
            {"LOWER": {"IN": ["with", "for"]}},
        ],
    ),
    ConTextItem("admitted to", "ADMISSION", rule="FORWARD",),
    ConTextItem("admitted on", "ADMISSION", rule="FORWARD"),
    ConTextItem(
        "Reason for ED visit or Hospital Admission:",
        "ADMISSION",
        rule="FORWARD",
        max_scope=2,
    ),
    ConTextItem("Reason for ICU:", "ADMISSION", rule="FORWARD"),
    ConTextItem(
        "in the hospital for for",
        "ADMISSION",
        rule="FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"IN": ["in", "to"]}},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": {"IN": ["hospital", "icu", "micu"]}},
            {"LOWER": "for"},
        ],
    ),
    ConTextItem(
        "in the hospital due to",
        "ADMISSION",
        rule="FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"IN": ["in", "to"]}},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": {"IN": ["hospital", "icu", "micu"]}},
            {"LOWER": "due"},
            {"LOWER": "to"},
        ],
    ),
    ConTextItem(
        "hospitalized for",
        "ADMISSION",
        rule="FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"REGEX": "hospitali"}},
            {"_": {"concept_tag": "timex"}, "OP": "*"},
            {"LOWER": "for"},
        ],
    ),
    ConTextItem(
        "hospitalized due to",
        "ADMISSION",
        rule="FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"REGEX": "hospitali"}},
            {"_": {"concept_tag": "timex"}, "OP": "*"},
            {"LOWER": "due"},
            {"LOWER": "to"},
        ],
    ),
    ConTextItem("admission for", "ADMISSION", rule="FORWARD"),
    ConTextItem(
        "management of", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=3
    ),
    ConTextItem(
        "history of travel",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"IN": ["hx", "-hx", "history"]}},
            {"LOWER": "of"},
            {"LOWER": "travel"},
        ],
        allowed_types={"location"},
    ),
    ConTextItem(
        "presumed positive",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^presum"}},
            {"LOWER": {"IN": ["pos", "positive", "+"]}, "OP": "?"},
        ],
    ),
    ConTextItem(
        "ARDS from",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": "ards"}, {"LOWER": {"IN": ["from", "with"]}, "OP": "?"}],
        allowed_types={"COVID-19"},
        max_scope=3,
    ),
    ConTextItem(
        "ARDS secondary to",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": "ards"}, {"LOWER": "secondary"}, {"LOWER": "to"}],
        allowed_types={"COVID-19"},
        max_scope=3,
    ),
    ConTextItem(
        "acute respiratory distress",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        max_scope=3,
    ),
    ConTextItem(
        "post-extubation", "DEFINITE_POSITIVE_EXISTENCE", rule="FORWARD", max_scope=3
    ),
    ConTextItem(
        "in the setting of",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
        pattern=[
            {"LOWER": "in"},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": "setting"},
            {"LOWER": "of"},
        ],
    ),
    ConTextItem(
        "in the s/o",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
    ),
    ConTextItem(
        "found to have",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
    ),
    ConTextItem(
        "presents with",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
        pattern=[{"LOWER": {"REGEX": "^present"}, "POS": "VERB"}, {"LOWER": "with"}],
    ),
    ConTextItem(
        "respiratory failure",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "resp"}},
            {"LOWER": "failure"},
            {"LOWER": {"IN": ["with", "due"]}, "OP": "?"},
            {"LOWER": "to", "OP": "?"},
        ],
        max_scope=4,
    ),
    ConTextItem(
        "respiratory failure 2/2",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "resp"}},
            {"LOWER": "failure"},
            {"LOWER": "(", "OP": "?"},
            {"LOWER": {"REGEX": "[12]/2"}},
            {"LOWER": ")", "OP": "?"},
        ],
        max_scope=4,
    ),
    ConTextItem(
        "active for",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": "active"}, {"LOWER": "for", "OP": "?"}],
        allowed_types={"COVID-19"},
        max_scope=2,
        on_match=callbacks.disambiguate_active,
    ),
    ConTextItem(
        "resolving", "DEFINITE_POSITIVE_EXISTENCE", rule="BACKWARD", max_scope=2
    ),
    ConTextItem(
        "recovering from",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[{"LOWER": {"IN": ["recovery", "recovering"]}}, {"LOWER": "from"}],
        max_scope=2,
    ),
    ConTextItem(
        "not recovered",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        pattern=[
            {"LOWER": "not"},
            {"LOWER": "yet", "OP": "?"},
            {"LOWER": {"REGEX": "^recover"}},
        ],
    ),
    ConTextItem(
        "Detected",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BACKWARD",
        max_targets=1,
        max_scope=5,
        pattern=[{"LOWER": {"REGEX": "^detected"}}],
        on_match=callbacks.check_no_x_detected,
    ),
    ConTextItem(
        "Value: Detected",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BACKWARD",
        max_targets=1,
        max_scope=5,
        pattern=[
            {"LOWER": "value"},
            {"LOWER": ":"},
            {"LOWER": {"REGEX": "^detected"}},
        ],
        on_match=callbacks.check_no_x_detected,
    ),
    ConTextItem(
        "POSITIVEH",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="BACKWARD",
        max_targets=1,
        max_scope=5,
    ),
    # "PATIENT_EXPERIENCER" modifiers will set is_positive to True
    # These will capture constructs such as "76-year-old male admitted for COVID-19"
    ConTextItem(
        "<NUM> yo with",
        "PATIENT_EXPERIENCER",
        rule="FORWARD",
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
    ConTextItem(
        "<NUM> yo with",
        "PATIENT_EXPERIENCER",
        rule="FORWARD",
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
    ConTextItem(
        "<NUM> y/o with",
        "PATIENT_EXPERIENCER",
        rule="FORWARD",
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
    ConTextItem(
        "<NUM>yo with",
        "PATIENT_EXPERIENCER",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "[\d]+yo"}},
            {"OP": "?"},  # "male/female/..."
            {"LOWER": {"IN": ["patient", "veteran"]}, "OP": "?"},
            {"LOWER": {"IN": ["with", "w", "w/"]}},
        ],
        max_scope=10,
    ),
    ConTextItem(
        "the patient has",
        "PATIENT_EXPERIENCER",
        rule="FORWARD",
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
    ConTextItem(
        "precaution",
        "FUTURE/HYPOTHETICAL",
        rule="BACKWARD",
        max_scope=2,
        pattern=[{"LOWER": {"REGEX": "precaution"}}],
    ),
    ConTextItem("precautions:", "IGNORE", rule="FORWARD", max_scope=2),
    ConTextItem(
        "precaution for",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "precaution|protection|protect"}},
            {"LOWER": {"IN": ["for", "against"]}},
        ],
    ),
    ConTextItem("concern about", "FUTURE/HYPOTHETICAL", rule="FORWARD"),
    ConTextItem("reports of", "FUTURE/HYPOTHETICAL", rule="FORWARD"),
    ConTextItem(
        "vaccine",
        "FUTURE/HYPOTHETICAL",
        rule="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),  # If they're talking about vaccines, it's probably just the patient asking
    ConTextItem("protect yourself", "FUTURE/HYPOTHETICAL", rule="FORWARD"),
    ConTextItem(
        "prevention",
        "FUTURE/HYPOTHETICAL",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^prevent"}}],
    ),
    ConTextItem("avoid", "FUTURE/HYPOTHETICAL", rule="FORWARD"),
    ConTextItem(
        "questions about",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "question"}},
            {"LOWER": {"IN": ["about", "regarding", "re", "concerning", "on", "for"]}},
        ],
        allowed_types={"COVID-19"},
    ),
    ConTextItem(
        "information about",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        max_scope=3,
        allowed_types={"COVID-19"},
        pattern=[{"LOWER": "information"}, {"LOWER": {"IN": ["about", "regarding"]}}],
    ),
    ConTextItem("anxiety about", "FUTURE/HYPOTHETICAL", rule="FORWARD"),
    ConTextItem(
        "ask about",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        pattern=[{"LOWER": {"REGEX": "^ask"}}, {"LOWER": "about"}],
        allowed_types={"travel", "COVID-19"},
    ),
    ConTextItem(
        "education",
        "FUTURE/HYPOTHETICAL",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^educat"}}],
    ),
    ConTextItem(
        "instruction",
        "FUTURE/HYPOTHETICAL",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "instruction"}}],
    ),
    ConTextItem(
        "information about",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        max_scope=3,
        pattern=[
            {"LOWER": "information"},
            {"LOWER": {"IN": ["on", "about", "regarding", "re"]}, "OP": "?"},
        ],
    ),
    ConTextItem("materials", "FUTURE/HYPOTHETICAL", rule="BIDIRECTIONAL",),
    ConTextItem("factsheet", "FUTURE/HYPOTHETICAL", rule="BIDIRECTIONAL",),
    ConTextItem("fact sheet", "FUTURE/HYPOTHETICAL", rule="BIDIRECTIONAL",),
    ConTextItem("protocol", "FUTURE/HYPOTHETICAL", rule="BIDIRECTIONAL", max_scope=3),
    ConTextItem("literature", "FUTURE/HYPOTHETICAL", rule="BIDIRECTIONAL"),
    ConTextItem(
        "handout",
        "FUTURE/HYPOTHETICAL",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^informat"}, "OP": "?"},
            {"LOWER": {"IN": ["handout", "handouts"]}},
        ],
    ),
    ConTextItem(
        "anxious about",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        pattern=[
            {"LOWER": {"IN": ["anxious", "worried", "worries", "worry", "worrying"]}},
            {"LOWER": {"IN": ["about", "re", "regarding"]}, "OP": "?"},
        ],
        allowed_types={"COVID-19",},
    ),
    ConTextItem(
        "if", "FUTURE/HYPOTHETICAL", rule="FORWARD", max_scope=10
    ),  # "If COVID-19 test is positive"
    ConTextItem(
        "advisory",
        "SCREENING",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["advisory", "advisories"]}}],
    ),
    ConTextItem("travel screen", "SCREENING", rule="BIDIRECTIONAL"),
    ConTextItem("travel screen:", "SCREENING", rule="BIDIRECTIONAL"),
    ConTextItem("Travel History Questionnaire", "SCREENING", rule="BIDIRECTIONAL"),
    ConTextItem("questionnaire:", "SCREENING", rule="BACKWARD", max_scope=2),
    ConTextItem(
        "questionnaire",
        "SCREENING",
        rule="BACKWARD",
        max_scope=2,
        pattern=[{"LOWER": {"REGEX": "questionn?aire"}}],
    ),
    ConTextItem(
        "questions",
        "SCREENING",
        rule="BACKWARD",
        max_scope=2,
        pattern=[{"LEMMA": "question"}],
    ),
    ConTextItem(
        "screening",
        "SCREENING",
        rule="BIDIRECTIONAL",
        max_scope=10,
        pattern=[{"LOWER": {"REGEX": "^screen"}}],
    ),
    ConTextItem(
        "prescreening",
        "SCREENING",
        rule="BIDIRECTIONAL",
        max_scope=None,
        pattern=[{"LOWER": {"REGEX": "prescreen"}}],
    ),
    ConTextItem("front gate", "SCREENING", rule="BIDIRECTIONAL",),
    ConTextItem("have you", "NOT_RELEVANT", rule="FORWARD",),
    # ConTextItem
    ConTextItem(
        "This patient was screened for the following suspected travel related illness(es):",
        "FUTURE/HYPOTHETICAL",
        rule="BIDIRECTIONAL",
    ),
    ConTextItem(
        "will be traveling",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        allowed_types={"location", "COVID-19"},
        pattern=[
            {"LOWER": "will"},
            {"LOWER": "be", "OP": "?"},
            {"LOWER": {"REGEX": "travel"}},
        ],
    ),
    ConTextItem(
        "travel plans",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        allowed_types={"location", "COVID-19"},
    ),
    ConTextItem(
        "if you need", "FUTURE/HYPOTHETICAL", rule="FORWARD"
    ),  # "If you need to be tested for"
    ConTextItem(
        "limit risk of",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        allowed_types={"COVID-19"},
        pattern=[
            {"LEMMA": {"IN": ["limit", "reduce", "lower", "minimize"]}},
            {"LOWER": "the", "OP": "?"},
            {"LEMMA": {"IN": ["risk", "chance", "possibility"]}},
            {"LEMMA": "of"},
        ],
    ),  # "If you need to be tested for"
    ConTextItem(
        "plan to travel",
        "FUTURE/HYPOTHETICAL",
        rule="FORWARD",
        allowed_types={"location", "COVID-19"},
        pattern=[
            {"LOWER": {"REGEX": "plan"}},
            {"LOWER": "to"},
            {"LOWER": {"REGEX": "travel"}},
        ],
    ),
    ConTextItem(
        "N years ago",
        "HISTORICAL",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LIKE_NUM": True, "OP": "?"},
            {"LOWER": {"IN": ["year", "years"]}},
            {"LOWER": "ago"},
        ],
    ),
    # Previously, these modifiers were set to be "HISTORICAL"
    # but are instead being marked as "POSITIVE" so that we identify any current
    # or past cases of COVID-19.
    ConTextItem(
        "history of",
        "DEFINITE_POSITIVE_EXISTENCE",
        rule="FORWARD",
        max_scope=4,
        pattern=[{"LOWER": {"IN": ["hx", "-hx", "history"]}}, {"LOWER": "of"}],
    ),
    ConTextItem(
        "(resolved)", "DEFINITE_POSITIVE_EXISTENCE", rule="BACKWARD", max_scope=1
    ),
    # ConTextItem("resolved", "DEFINITE_POSITIVE_EXISTENCE", rule="BIDIRECTIONAL", max_scope=3),
    # ConTextItem("20XX", "HISTORICAL", rule="BIDIRECTIONAL", max_scope=5,
    #             pattern=[{"TEXT": {"REGEX": "20[01][0-8]"}}]),
    ConTextItem(
        "in 20XX",
        "HISTORICAL",
        rule="BIDIRECTIONAL",
        max_scope=5,
        pattern=[{"LOWER": "in"}, {"OP": "?"}, {"TEXT": {"REGEX": "^20[01][0-9]$"}}],
    ),
    # The following modifiers try to capture instances where a health department
    # or infection control team was contacted
    ConTextItem(
        "contacted",
        "COMMUNICATION",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["contacted", "contact"]}, "POS": "VERB"}],
        allowed_types={"health department"},
        # on_match=callbacks.di,
    ),  # TODO: may have to disambiguate this with "came in contact"
    ConTextItem(
        "contact",
        "CONTACT",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": "contact", "POS": "NOUN"}],
        allowed_types={"COVID-19"},
        on_match=callbacks.disambiguate_contact,
    ),
    ConTextItem(
        "call",
        "COMMUNICATION",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^call"}}],
        allowed_types={"health department"},
    ),
    ConTextItem(
        "was contacted",
        "COMMUNICATION",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["was", "been"]}}, {"LOWER": "contacted"}],
        allowed_types={"health department"},
    ),
    ConTextItem(
        "notified",
        "COMMUNICATION",
        rule="BIDIRECTIONAL",
        allowed_types={"health department"},
    ),
    ConTextItem(
        "communicate with",
        "COMMUNICATION",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^communicate"}},
            {"LOWER": {"IN": ["with", "w"]}},
            {"LOWER": "/", "OP": "?"},
        ],
        allowed_types={"health department"},
    ),
    ConTextItem(
        "sent to",
        "COMMUNICATION",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": "sent"}, {"OP": "?"}, {"LOWER": "to"}],
        allowed_types={"health department"},
    ),
    ConTextItem(
        "sent",
        "COMMUNICATION",
        rule="BIDIRECTIONAL",
        allowed_types={"health department"},
    ),
    ConTextItem(
        "spoke with",
        "COMMUNICATION",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": "spoke"}, {"LOWER": {"IN": ["with", "to"]}}],
        allowed_types={"health department"},
    ),
    ConTextItem(
        "consulted",
        "COMMUNICATION",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "consult"}}, {"LOWER": "with", "OP": "?"}],
        allowed_types={"health department"},
    ),
    ConTextItem(
        "test for",
        "TEST",
        rule="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^test"}}, {"LOWER": "for", "OP": "?"}],
    ),
    ConTextItem(
        "retest for",
        "TEST",
        rule="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^retest"}}, {"LOWER": "for", "OP": "?"}],
    ),
    ConTextItem(
        "check for",
        "TEST",
        rule="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^check"}, "POS": "VERB"}, {"LOWER": "for"}],
    ),
    ConTextItem(
        "work up",
        "TEST",
        pattern=[{"LOWER": "work"}, {"LOWER": "-", "OP": "?"}, {"LOWER": "up"}],
    ),
    ConTextItem("workup", "TEST"),
    ConTextItem("results", "TEST", "BACKWARD", max_scope=2),
    ConTextItem(
        "evaluation",
        "TEST",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=2,
    ),
    ConTextItem(
        "evaluated for",
        "TEST",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^eval"}}, {"LOWER": "for"}],
    ),
    ConTextItem(
        "swab",
        "TEST",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^swab"}}],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "PCR",
        "TEST",
        rule="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "specimen sent",
        "TEST",
        rule="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem("awaiting results", "UNCERTAIN", rule="BIDIRECTIONAL"),
    ConTextItem(
        "at risk for",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "risk for",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        # terminated_by={"DEFINITE_POSITIVE_EXISTENCE"}
    ),
    ConTextItem(
        "risk",
        "UNCERTAIN",
        "BACKWARD",
        max_scope=1,
        pattern=[{"LOWER": {"IN": ["risk", "risks"]}}],
    ),
    ConTextItem(
        "risk factors for",
        "UNCERTAIN",
        "FORWARD",
        max_scope=5,
        pattern=[{"LOWER": "risk"}, {"LEMMA": "factor"}, {"LOWER": "for"}],
    ),
    ConTextItem("investigation of", "UNCERTAIN", "FORWARD", max_scope=1),
    ConTextItem("to exclude", "UNCERTAIN", "FORWARD",),
    ConTextItem("awaiting", "UNCERTAIN", "BIDIRECTIONAL", max_scope=2),
    ConTextItem("question of", "UNCERTAIN", "FORWARD", max_scope=4),
    ConTextItem("differential diagnosis:", "UNCERTAIN", "FORWARD", max_scope=4),
    ConTextItem("ddx:", "UNCERTAIN", "FORWARD", max_scope=4),
    ConTextItem(
        "currently being ruled out or has tested positive for",
        "UNCERTAIN",
        "BIDIRECTIONAL",
    ),
    ConTextItem(
        "person of interest",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        pattern=[
            {"LEMMA": {"IN": ["person", "patient"]}},
            {"LOWER": "of"},
            {"LOWER": "interest"},
        ],
    ),
    ConTextItem("under investigation", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextItem(
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
    ConTextItem(
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
    ConTextItem(
        "area with",
        "OTHER_EXPERIENCER",
        pattern=[
            {"LOWER": {"IN": ["area", "county", "comsmunity", "city"]}},
            {"LOWER": {"IN": ["with", "of"]}},
        ],
    ),
    ConTextItem(
        "facility with",
        "OTHER_EXPERIENCER",
        "FORWARD",
        pattern=[
            {"LOWER": "facility"},
            {"LOWER": {"IN": ["with", "has"]}},
            {"LOWER": "a"},
        ],
    ),
    ConTextItem("known to have", "OTHER_EXPERIENCER", "FORWARD"),
    ConTextItem(
        "same room",
        "OTHER_EXPERIENCER",
        pattern=[{"LOWER": "same"}, {"OP": "?"}, {"LOWER": {"REGEX": "room"}}],
    ),
    ConTextItem("in the building", "OTHER_EXPERIENCER", "BIDIRECTIONAL"),
    ConTextItem(
        "several residents",
        "OTHER_EXPERIENCER",
        "FORWARD",
        pattern=[{"LOWER": {"IN": ["multiple", "several"]}}, {"LOWER": "residents"}],
    ),
    ConTextItem(
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
    ConTextItem("patients with", "OTHER_EXPERIENCER", "FORWARD",),
    ConTextItem(
        "travel",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["flew", "traveled", "travelled"]}}],
    ),
    ConTextItem("got back from", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextItem("was recently in", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextItem(
        "positive screen",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "positive criteria",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "positive triage",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "pending",
        "UNCERTAIN",
        rule="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^test"}, "OP": "?"}, {"LOWER": "pending"}],
    ),
    ConTextItem(
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
    ConTextItem(
        "possible",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "possibly",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "possible positive",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "possibl"}}, {"LOWER": "positive"}],
    ),
    ConTextItem(
        "risk of",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextItem(
        "likely",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextItem(
        "probable",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextItem(
        "probably",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextItem(
        "questionnaire",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=2,
    ),
    ConTextItem(
        "suspicion",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "suspect",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^suspect"}}],
    ),
    ConTextItem(
        "suspicious for",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem("differential diagnosis", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextItem(
        "differential diagnosis",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        pattern=[{"LOWER": "ddx"}, {"LOWER": ":", "OP": "?"}],
    ),
    ConTextItem("symptoms", "SYMPTOM", max_scope=4,),
    ConTextItem(
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
    ConTextItem(
        "s/s", "UNCERTAIN", "BIDIRECTIONAL", allowed_types={"COVID-19"}, max_scope=5
    ),
    ConTextItem(
        "sx", "UNCERTAIN", "BIDIRECTIONAL", allowed_types={"COVID-19"}, max_scope=5
    ),
    ConTextItem(
        "potential",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^potential"}}],
    ),
    ConTextItem(
        "possible exposure",
        "UNCERTAIN",
        "BIDIRECTIONAL",  # allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[
            {"LOWER": {"IN": ["possible", "potential"]}},
            {"OP": "?"},
            {"LOWER": "exposure"},
        ],
    ),
    ConTextItem(
        "exposure",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^exposure"}}],
        on_match=callbacks.disambiguate_exposure,
    ),
    ConTextItem(
        "may have been exposed",
        "UNCERTAIN",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
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
    ConTextItem(
        "concern for",
        "UNCERTAIN",
        "FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"IN": ["concern"]}}, {"LOWER": {"IN": ["of", "for"]}}],
    ),
    ConTextItem("concerns", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextItem("if positive", "UNCERTAIN", "BIDIRECTIONAL"),
    ConTextItem("if negative", "UNCERTAIN", "BIDIRECTIONAL"),
    # ConTextItem("if", "UNCERTAIN", "BIDIRECTIONAL", max_scope=5), # "if his covid-19 is positive"
    ConTextItem("if you", "FUTURE/HYPOTHETICAL", "FORWARD"),
    ConTextItem(
        "c/f", "UNCERTAIN", "FORWARD", allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "assessed for",
        "UNCERTAIN",
        "FORWARD",
        pattern=[{"LOWER": {"IN": ["assess", "assessed"]}}, {"LOWER": "for"}],
    ),
    ConTextItem("concerning for", "UNCERTAIN", rule="FORWARD"),
    ConTextItem("r/o", "UNCERTAIN", rule="BIDIRECTIONAL", max_scope=2,),
    ConTextItem("r/o.", "UNCERTAIN", rule="BIDIRECTIONAL", max_scope=2,),
    ConTextItem(
        "rule out",
        "UNCERTAIN",
        rule="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
        pattern=[{"LEMMA": "rule"}, {"TEXT": "-", "OP": "?"}, {"LOWER": "out"}],
    ),
    ConTextItem(
        "ro",
        "UNCERTAIN",
        rule="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=2,
    ),
    ConTextItem(
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
    ConTextItem(
        "vs.",
        "UNCERTAIN",
        rule="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
        pattern=[{"LOWER": {"REGEX": "^(vs\.?|versus)$"}}],
    ),
    # certainty = low
    ConTextItem("unlikely", "UNLIKELY", "BIDIRECTIONAL"),
    ConTextItem("unlikely to be", "UNLIKELY", "FORWARD"),
    ConTextItem(
        "doubt", "UNLIKELY", "FORWARD", allowed_types={"COVID-19", "OTHER_CORONAVIRUS"}
    ),
    ConTextItem(
        "doubtful",
        "UNLIKELY",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem(
        "unlikely to be positive",
        "UNLIKELY",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextItem("low suspicion", "UNLIKELY", "BIDIRECTIONAL"),
    ConTextItem("low probability", "UNLIKELY", "BIDIRECTIONAL"),
    ConTextItem(
        "not recommend",
        "UNLIKELY",
        "FORWARD",
        pattern=[
            {"LOWER": "not"},
            {"LOWER": "recommend"},
            {"LOWER": {"REGEX": "test"}},
        ],
    ),
    ConTextItem("extremely low", "UNLIKELY", "BACKWARD", max_scope=3),
    ConTextItem("low risk of", "UNLIKELY", "FORWARD", max_scope=3),
    ConTextItem("is unlikely", "UNLIKELY", "BACKWARD"),
    ConTextItem(
        "low risk of",
        "UNLIKELY",
        "FORWARD",
        pattern=[{"LOWER": "low"}, {"LOWER": "risk"}, {"LOWER": {"IN": ["in", "for"]}}],
    ),
    ConTextItem(
        "positive patients",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["pos", "positive", "+"]}},
            {"LOWER": {"IN": ["pts", "patients"]}},
        ],
    ),
    ConTextItem(
        "patients",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        max_scope=10,
        pattern=[{"LOWER": {"IN": ["pts", "patients"]}}],
    ),
    ConTextItem(
        "other person",
        "OTHER_EXPERIENCER",
        "FORWARD",
        pattern=[{"_": {"concept_tag": "other_experiencer"}, "OP": "+"},],
    ),
    ConTextItem(
        "family member",
        "OTHER_EXPERIENCER",
        "FORWARD",
        pattern=[{"_": {"concept_tag": "family"}, "OP": "+"},],
        on_match=callbacks.family_speaker,
    ),
    ConTextItem(
        "<OTHER_EXPERIENCER> tested positive",
        "OTHER_EXPERIENCER",
        pattern=[
            {"_": {"concept_tag": {"IN": ["other_experiencer", "family"]}}, "OP": "+"},
            {"LOWER": {"REGEX": "^test"}},
            {"_": {"concept_tag": "positive"}, "OP": "+"},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextItem(
        "other patient",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "other"}},
            {"LOWER": {"REGEX": "(patient|resident|veteran|soldier)"}},
        ],
    ),
    ConTextItem(
        "a patient",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": "a"},
            {"LOWER": {"IN": ["patient", "pt", "pt.", "resident"]}},
        ],
    ),
    ConTextItem("any one", "OTHER_EXPERIENCER", "BIDIRECTIONAL", max_scope=100),
    ConTextItem(
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
    ConTextItem("had contact", "OTHER_EXPERIENCER", "BIDIRECTIONAL", max_scope=1000,),
    ConTextItem("same building", "OTHER_EXPERIENCER", "BIDIRECTIONAL", max_scope=1000,),
    ConTextItem("same floor", "OTHER_EXPERIENCER", "BIDIRECTIONAL", max_scope=1000,),
    ConTextItem(
        "cared for",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",  # The patient is a nurse who cared for a patient with COVID-19
        pattern=[{"LEMMA": "care"}, {"LOWER": "for"}],
    ),
    ConTextItem(
        "the woman/man",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["a", "the"]}},
            {"LOWER": {"IN": ["man", "men", "woman", "women"]}},
        ],
    ),
    ConTextItem(
        "XXmate",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",  # "roommate", "housemate", etc...
        pattern=[{"LOWER": {"REGEX": "mates?$"}}],
    ),
    ConTextItem(
        "clean",
        "OTHER_EXPERIENCER",
        "BIDIRECTIONAL",
        pattern=[{"LEMMA": "clean", "POS": "VERB"}],
    ),  # "She has been cleaning covid-19 positive rooms"
    ConTextItem(
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
    # ConTextItem("request", "FUTURE/HYPOTHETICAL", "FORWARD", pattern=[{"LEMMA": "request"}]),
    ConTextItem(
        "concerned about",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        pattern=[{"LOWER": {"REGEX": "concern"}}, {"LOWER": "about"}],
        max_scope=3,
    ),
    ConTextItem(
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
    ConTextItem(
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
    ConTextItem(
        "she would like",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        pattern=[{"POS": "PRON"}, {"LOWER": "would"}, {"LOWER": "like"}],
    ),
    ConTextItem(
        "desires", "FUTURE/HYPOTHETICAL", "FORWARD", pattern=[{"LEMMA": "desire"}]
    ),
    ConTextItem(
        "concerned for",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        pattern=[{"LOWER": "concerned"}, {"LOWER": "for"}],
    ),
    ConTextItem(
        "prepare for",
        "FUTURE/HYPOTHETICAL",
        "FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "prepare"}},
            {"LOWER": {"IN": ["for", "against"]}},
        ],
    ),
    ConTextItem("mers", "NOT_RELEVANT", "FORWARD", allowed_types={"COVID-19"}),
    ConTextItem(
        "seen in", "NOT_RELEVANT", "FORWARD", allowed_types={"COVID-19"}, max_scope=2
    ),  # "commonly seen in COVID-19 pneumonia"
    ConTextItem(
        "seen in the setting of",
        "NOT_RELEVANT",
        rule="FORWARD",
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
    ConTextItem(
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
    ConTextItem(
        "cancel vacation",
        "FUTURE/HYPOTHETICAL",
        rule="BIDIRECTIONAL",
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
    ConTextItem(
        "supposed to travel",
        "NOT_RELEVANT",
        rule="BIDIRECTIONAL",
        pattern=[
            {"LOWER": "supposed"},
            {"LOWER": "to"},
            {"LOWER": {"IN": ["travel", "go", "visit"]}},
        ],
    ),
    ConTextItem("called off", "FUTURE/HYPOTHETICAL", rule="BIDIRECTIONAL"),
    ConTextItem("goals:", "FUTURE/HYPOTHETICAL", rule="FORWARD"),
    ConTextItem(
        "a positive case of",
        "NOT_RELEVANT",
        "FORWARD",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextItem(
        "a confirmed case of",
        "NOT_RELEVANT",
        "FORWARD",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextItem(
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
    ConTextItem(
        "in the area",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": "in"},
            {"LOWER": "the"},
            {"LOWER": {"IN": ["area", "community"]}},
        ],
    ),
    ConTextItem(
        "cases",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextItem(
        "outbreak of",
        "NOT_RELEVANT",
        "FORWARD",
        allowed_types={"COVID-19"},
        max_scope=1,
    ),
    ConTextItem(
        "outbreak",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextItem(
        "epidemic",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextItem(
        "pandemic",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextItem(
        "national emergency",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextItem(
        "crisis",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextItem(
        "situation",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextItem(
        "mandate",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
        pattern=[{"LOWER": {"REGEX": "mandate"}}],
    ),
    ConTextItem(
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
    ConTextItem("clinic cancellation", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # ConTextItem("flight/trip", "NOT_RELEVANT", "BIDIRECTIONAL", allowed_types={"COVID-19"},
    #             pattern=[{"LOWER": {"IN": ["flight", "flights",
    #                                        "trip", "trips",
    #                                 "vacation", "vacations"]}}]), # "cancelled his flight because of coronavirus"
    ConTextItem(
        "read about",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        pattern=[{"LOWER": {"REGEX": "^read"}}, {"LOWER": "about"}],
    ),
    ConTextItem(
        "deployment",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "deploy"}}],
        allowed_types={"COVID-19"},
    ),
    # ConTextItem("current events", "NOT_RELEVANT", "BIDIRECTIONAL",
    #             pattern=[{"LOWER": {"IN": ["current", "recent"]}},
    #                      {"LOWER": {"REGEX": "^event"}}]), # Discussing current events for cognitive understanding
    # ConTextItem("topics", "NOT_RELEVANT", "BIDIRECTIONAL",
    #             pattern=[{"LOWER": {"REGEX": "^topic"}}]), # Discussing current events for cognitive understanding
    ConTextItem(
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
    ConTextItem("?", "NOT_RELEVANT", "BACKWARD", max_scope=2),
    # ConTextItem("in the last 14 days", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextItem("have you had close contact", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # 'Checkup done via telephone because of COVID-19.'
    # Won't match: 'Pt notified via telephone of his positive COVID-19 result.'
    # ConTextItem("telephone", "NOT_RELEVANT", "BIDIRECTIONAL", pattern=[{"LOWER": {"IN": ["telephone", "telehealth"]}}],
    #             on_match=callbacks.check_telephone_notification),
    ConTextItem("the group", "NOT_RELEVANT", "FORWARD"),  # Group therapy sessions
    ConTextItem(
        "session", "NOT_RELEVANT", "FORWARD", pattern=[{"LOWER": {"REGEX": "^session"}}]
    ),  # Group therapy sessions
    # ConTextItem("mental health", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextItem("website", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextItem("web site", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextItem("internet", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # ConTextItem("global", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextItem("worldwide", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextItem("world wide", "NOT_RELEVANT", "BIDIRECTIONAL"),
    ConTextItem("world-wide", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # "Patients with confirmed covid-19 should stay home"
    ConTextItem(
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
    ConTextItem(
        "nurse notes:",
        "NOT_RELEVANT",
        "FORWARD",  # often precedes a screening
        pattern=[{"LOWER": {"IN": ["nurse", "nurses", "rn"]}}, {"LOWER": "notes"}],
    ),
    # ConTextItem("mental health", "NOT_RELEVANT", "BIDIRECTIONAL",
    #             pattern=[{"LOWER": {"IN": ["psychiatry", "psychotic", "paranoid", "paranoia", "psych"]}}]),
    ConTextItem("countries with cases", "NOT_RELEVANT", "BIDIRECTIONAL"),
    # ConTextItem(":", "NOT_RELEVANT", "BACKWARD", max_scope=1), # "Coronavirus: ..."
    ConTextItem(
        "cases of", "NOT_RELEVANT", "FORWARD", max_scope=3
    ),  # "his daughter lives in Seoul, where cases of coronavirus have been discovered"
    # ConTextItem("alert and oriented", "NOT_RELEVANT", "FORWARD"),
    # ConTextItem("the", "NOT_RELEVANT", "FORWARD", max_scope=1, allowed_types={"COVID-19"}), # When clinicians are relaying a patient's anxieties or questions, they often use 'the coronavirus', whereas when they're using their own clinical judgment they just say 'coronavirus'
    ConTextItem(
        "been in contact with anyone confirmed", "NOT_RELEVANT", "BIDIRECTIONAL"
    ),
    ConTextItem(
        "error", "NOT_RELEVANT", "BIDIRECTIONAL"
    ),  # "COVID-19 marked positive in error"
    ConTextItem(
        "elective", "NOT_RELEVANT", "BIDIRECTIONAL", max_scope=5
    ),  # "elective surgeries will be scheduled after COVID-19 has ended"
    ConTextItem(
        "rescheduled",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        pattern=[{"LEMMA": "reschedule"}],
    ),
    ConTextItem(
        "postponed", "NOT_RELEVANT", "BIDIRECTIONAL", pattern=[{"LEMMA": "postpone"}]
    ),
    ConTextItem(
        "barriers to travel",
        "NOT_RELEVANT",
        "BIDIRECTIONAL",
        pattern=[{"LEMMA": "barrier"}, {"LOWER": "to"}, {"LOWER": "travel"}],
    ),
    # Contact with sick individuals
    ConTextItem(
        "positive individual",
        "CONTACT",
        "BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["positive", "+", "confirmed"]}, "POS": "ADJ"},
            {"LEMMA": {"IN": ["individual", "contact", "patient"]}},
        ],
    ),
    ConTextItem(
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
    ConTextItem(
        "contact with",
        "CONTACT",
        "FORWARD",
        pattern=[{"LOWER": "contact"}, {"LOWER": {"REGEX": "w(/|ith)?$"}}],
    ),
    ConTextItem("social worker", "IGNORE", "BIDIRECTIONAL"),
    ConTextItem("initially negative", "IGNORE", "BIDIRECTIONAL"),
    ConTextItem("likely recovered", "IGNORE", "BIDIRECTIONAL"),
    ConTextItem("not aware", "IGNORE", "BIDIRECTIONAL"),
    ConTextItem("positive cases", "IGNORE", "BIDIRECTIONAL"),
    ConTextItem("client history", "IGNORE", "BIDIRECTIONAL"),
    ConTextItem("emergency contact", "IGNORE", "BIDIRECTIONAL"),
    ConTextItem("several positive", "IGNORE", "BIDIRECTIONAL"),
    ConTextItem("special instructions:", "IGNORE", "BIDIRECTIONAL"),
    ConTextItem(
        "positive symptoms",
        "IGNORE",
        "BIDIRECTIONAL",
        pattern=[{"LOWER": "positive"}, {"LOWER": {"REGEX": "symptom|sign"}}],
    ),
    # Ignore "history" in "history of present illness"
    ConTextItem(
        "history of present illness", "IGNORE", "TERMINATE", allowed_types={"COVID-19"}
    ),
    ConTextItem("does not know", "IGNORE", "TERMINATE"),
    ConTextItem(
        "benign", "SPECIFIED_STRAIN", "BIDIRECTIONAL", allowed_types={"COVID-19"}
    ),
    ConTextItem("but", "CONJ", "TERMINATE"),
    ConTextItem("therefore", "CONJ", "TERMINATE"),
    ConTextItem(";", "CONJ", "TERMINATE"),
    # "Positive for X" should terminate
    ConTextItem("Metapneumovirus", "CONJ", "TERMINATE"),
    ConTextItem(
        "flu", "CONJ", "TERMINATE", pattern=[{"LOWER": {"REGEX": "flu"}}]
    ),  # Stop modifiers for flu
    # ConTextItem("who", "CONJ", "TERMINATE"), # example: "male with history of afib, who recently came back from China"
]
