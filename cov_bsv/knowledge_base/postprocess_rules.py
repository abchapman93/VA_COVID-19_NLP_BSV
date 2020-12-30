from medspacy.postprocess import PostprocessingRule, PostprocessingPattern
from medspacy.postprocess import postprocessing_functions
import re


def has_positive_tag(ent):
    return has_tag(ent, "positive")


def has_tag(ent, target):
    target = target.lower()
    for token in ent:
        if token._.concept_tag.lower() == target:
            return True
    return False


def has_positive(ent):
    """Returns True if an entity is either modified by 'DEFINITE_POSITIVE_EXISTENCE',
    is_positive is True, or there is a 'positive' token in the span.
    """
    if ent._.is_positive is True:
        return True
    if postprocessing_functions.is_modified_by_category(
        ent, "DEFINITE_POSITIVE_EXISTENCE"
    ):
        return True
    if has_positive_tag(ent):
        return True
    return False


def next_sentence_contains(ent, target):
    next_sent = get_next_sentence(ent)
    if next_sent is None:
        return False
    return postprocessing_functions.span_contains(next_sent, target)


def next_sentence_starts_with(ent, target, max_dist=None, window=1):
    next_sent = get_next_sentence(ent)
    if next_sent is None:
        return False
    if max_dist is not None and next_sent.start - ent.end > max_dist:
        return False
    if not isinstance(target, str):
        target = "|".join(target)
    # print(next_sent[:window])
    return re.search(target, next_sent[:window].text, re.IGNORECASE) is not None


def get_next_sentence(ent):
    sent = ent.sent
    try:
        return ent.doc[sent.end].sent
    except IndexError:
        return None


def get_preceding_span(ent, window):
    if ent.start - window < 0:
        return ent.doc[: ent.start]
    return ent.doc[ent.start - window : ent.start]


def set_is_positive(ent, i, value=True):
    ent._.is_positive = value


def set_is_future(ent, i, value=True):
    ent._.is_future = value


def set_is_uncertain(ent, i, value=True):
    ent._.is_future = value


def ent_is_sent_start(ent):
    "Returns True if a span contains a token which is a sentence start."
    for token in ent:
        if token.is_sent_start:
            return True
    return False


postprocess_rules = [
    PostprocessingRule(
        patterns=[PostprocessingPattern(lambda ent: ent.label_.upper() == "IGNORE")],
        action=postprocessing_functions.remove_ent,
        description="Remove any entities which were tagged to be ignored.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_text,
                condition_args=("education",),
            )
        ],
        action=postprocessing_functions.remove_ent,
        description="Remove any entities which are modified by 'education'",
    ),
    PostprocessingRule(
        patterns=[
            # PostprocessingPattern(postprocessing_functions.is_followed_by, condition_args=("?",2))
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(lambda ent: "?" in ent.sent.lower_[-3:]),
        ],
        action=postprocessing_functions.remove_ent,
        description="Remove any entities which are followed by a question mark since this are often screenings.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.sentence_contains,
                condition_args=({"deny", "denies", "denied"},),
            ),
            PostprocessingPattern(
                postprocessing_functions.sentence_contains,
                condition_args=({"contact", "contacts", "confirmed"},),
            ),
        ],
        action=postprocessing_functions.remove_ent,
        description="Remove a coronavirus entity if 'denies' and 'contact' are in. This will help get rid of false positives from screening.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            # PostprocessingPattern(postprocessing_functions.is_modified_by_category,
            #                           condition_args=("DEFINITE_POSITIVE_EXISTENCE",), success_value=False),
            PostprocessingPattern(
                has_tag, condition_args=("positive",), success_value=False
            ),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_text,
                condition_args=("(setting of|s/o)",),
            ),
            PostprocessingPattern(
                postprocessing_functions.ent_contains,
                condition_args=({"infection", "pneumonia", "ards"},),
                success_value=False,
            ),
        ],
        action=set_is_positive,
        action_args=(False,),
        description="Only allow 'setting of' to modify entities which have a specific clinical phrase such as 'infection'. "
        "This will disambiguate between phrases like 'Life has changed in the setting of COVID-19' vs. "
        "'Pt presents to ED in the setting of COVID-19 infection.'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(lambda ent: ent._.section_category in ["diagnoses", "problem_list", "past_medical_history"]),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("TEST",),
            ),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("DEFINITE_POSITIVE_EXISTENCE",),
                success_value=False,
            ),
            PostprocessingPattern(has_positive_tag, success_value=False),
        ],
        action=set_is_uncertain,
        action_args=(True,),
        description="If a mention of COVID testing occurs in a positive section but doesn't have any "
                    "additional positive modifiers, set uncertain to True. "
                    "Example: 'Diagnoses: COVID-19 testing'"
        # TODO: Might want to modify the logic for sections so that it doesn't immediately assign is_positive to all spans.
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("SCREENING",),
            ),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("TEST",),
            ),
            PostprocessingPattern(lambda ent: ent._.is_positive is True),
        ],
        action=set_is_uncertain,
        action_args=(False,),
        description="If coronavirus is modified by 'screening', 'test' and 'positive', change the certainty to certain. "
        "Example: 'Pt was screened for covid and later tested positive.'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("SPECIFIED_STRAIN",),
            ),
        ],
        action=postprocessing_functions.set_label,
        action_args=("specified coronavirus",),
        description="Example: Tested for positive coronavirus benign, not the novel strain.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("test",),
            ),
            PostprocessingPattern(has_positive, success_value=False),
            (
                PostprocessingPattern(
                    next_sentence_contains,
                    condition_args=("results? (are|is) positive",),
                ),
                PostprocessingPattern(
                    next_sentence_contains, condition_args=("results pos[^s]",)
                ),
            ),
        ],
        action=set_is_positive,
        action_args=(True,),
        description="If a test does not have any results within the same sentence, check the next sentence.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("test",),
            ),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("DEFINITE_POSITIVE_EXISTENCE",),
                success_value=False,
            ),
            PostprocessingPattern(has_positive_tag, success_value=False),
            (
                PostprocessingPattern(
                    postprocessing_functions.is_modified_by_category,
                    condition_args=("ADMISSION",),
                ),
                PostprocessingPattern(
                    postprocessing_functions.is_modified_by_category,
                    condition_args=("PATIENT_EXPERIENCER",),
                ),
            ),
        ],
        action=set_is_uncertain,
        action_args=(True,),
        description="If a patient is admitted for testing and it is not positive, set to uncertain.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("NEGATED_EXISTENCE",),
            ),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_text,
                condition_args=("pending",),
            ),
        ],
        action=postprocessing_functions.set_negated,
        action_args=(False,),
        description="If a coronavirus entity is negated but also has 'pending' in the sentence, set is_negated to False. It should be uncertain.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("DEFINITE_POSITIVE_EXISTENCE",),
            ),
            # PostprocessingPattern(postprocessing_functions.is_modified_by_category, condition_args=("TEST",)),
            PostprocessingPattern(
                postprocessing_functions.sentence_contains,
                condition_args=(
                    {
                        "should",
                        "unless",
                        "either",
                        "if comes back",
                        "if returns",
                        "if s?he tests positive",
                    },
                    True,
                ),
            ),
        ],
        action=set_is_uncertain,
        action_args=(True,),
        description="Subjunctive of test returning positive. 'Will contact patient should his covid-19 test return positive.'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(lambda ent: ent._.is_positive is False),
            PostprocessingPattern(
                next_sentence_starts_with,
                condition_args=(r"(\+|pos\b|positive|detected)", 5, 1),
            ),
            # PostprocessingPattern(lambda ent: postprocessor.next_sentence_starts_with(ent) is not None and "+" in postprocessor.get_next_sentence(ent)[:3].text),
        ],
        action=set_is_positive,
        description="Sentences often incorrectly split on '+', leading to false negatives",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            (
                PostprocessingPattern(
                    postprocessing_functions.is_modified_by_category,
                    condition_args=("DEFINITE_POSITIVE_EXISTENCE",),
                ),
                PostprocessingPattern(has_tag, condition_args=("positive",)),
            ),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_text,
                condition_args=("precaution", True),
            ),
        ],
        action=set_is_future,
        action_args=(False,),
        description="Differentiate 'COVID + precautions' from 'COVID precautions'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.sentence_contains,
                condition_args=("admitted to covid unit",),
            ),
        ],
        action=set_is_positive,
        action_args=(True,),
        description="If a patient is admitted to the covid unit with covid, count as positive",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_text,
                condition_args=("pending",),
            ),
            PostprocessingPattern(
                postprocessing_functions.sentence_contains, condition_args=(["retest"],)
            ),
        ],
        action=set_is_uncertain,
        action_args=(False,),
        description="If a patient has a retest pending, modify the COVID certainty to 'certain'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(lambda ent: ent._.is_positive is False,),
            PostprocessingPattern(ent_is_sent_start),
            PostprocessingPattern(
                lambda ent: has_positive_tag(get_preceding_span(ent, 3))
            ),
        ],
        action=set_is_positive,
        action_args=(True,),
        description="Bad sentence splitting sometimes splits on 'Covid' and separates a positive result, "
        "so look in the beginning of the next sentence.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("SCREENING",),
            ),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("TEST",),
                success_value=False,
            ),
            PostprocessingPattern(lambda ent: ent._.is_positive is True),
            PostprocessingPattern(
                has_tag, condition_args=("positive",), success_value=False
            ),  # If the positive modifier is actually part of the entity, then fail
            PostprocessingPattern(
                has_tag, condition_args=("associated_diagnosis",), success_value=False
            ),  # If the positive modifier is actually part of the entity, then fail
        ],
        action=postprocessing_functions.set_label,
        action_args=("positive coronavirus screening",),
        description="If coronavirus is modified by both 'screening' and 'positive', change the label to 'POSITIVE CORONAVIRUS SCREENING'.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("NEGATED_EXISTENCE",),
            ),
            PostprocessingPattern(has_positive),
            PostprocessingPattern(
                postprocessing_functions.sentence_contains,
                condition_args=(["re[ -]?test", "second test", "repeat"],),
            ),
        ],
        action=postprocessing_functions.set_negated,
        action_args=(False,),
        description="If COVID-19 is positive but a repeat is negative, consider it positive and set is_negated to False.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            (
                PostprocessingPattern(
                    postprocessing_functions.is_modified_by_category,
                    condition_args=("DEFINITE_POSITIVE_EXISTENCE",),
                ),
                PostprocessingPattern(has_positive_tag,),
            ),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_text,
                condition_args=(["sign", "symptom", "s/s"],),
            ),
            PostprocessingPattern(
                postprocessing_functions.is_followed_by, condition_args=("with", 3)
            ),
        ],
        action=set_is_uncertain,
        action_args=(True,),
        description="If a patient is positive for 'covid-19 with signs/symptoms', set certainty to True.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_ == "COVID-19"),
            PostprocessingPattern(lambda ent: "symptom" in ent.lower_),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_category,
                condition_args=("DEFINITE_POSITIVE_EXISTENCE",),
            ),
            PostprocessingPattern(
                postprocessing_functions.is_modified_by_text, condition_args=("test",)
            ),
        ],
        action=set_is_uncertain,
        action_args=(True,),
        description="Set certainty to True for phrases like 'COVID-19 symptoms and positive test'.",
    ),
]
