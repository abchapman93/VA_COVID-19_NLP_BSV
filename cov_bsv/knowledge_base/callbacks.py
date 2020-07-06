from medspacy.postprocess import postprocessing_functions


def disambiguate_confirmed(matcher, doc, i, matches):
    """Disambiguate the phrase 'confirmed' to avoid ambiguity
    of 'confirmed  for appointment' vs. 'confirmed COVID-19'.
    """
    (_, start, end) = matches[i]
    span = doc[start:end]
    # If this precedes a target concept, return True
    try:
        next_token = doc[i + 1]
        if next_token.lower_ in ["coronavirus", "covid-19", "covid", "sars-cov2"]:
            return
        if next_token.lower_ in ["that"]:
            matches.pop(i)
            return
    except IndexError:
        pass

    for text in [
        "appointment",
        "appt",
        "schedule",
        "phone",
        "telephone",
        "called",
        "ident",
    ]:
        if text in span.sent.lower_:
            matches.pop(i)
            return


def disambiguate_positive(matcher, doc, i, matches):
    """Check if mental health phrases occur with 'positive'
    """

    (_, start, end) = matches[i]
    span = doc[start:end]

    if postprocessing_functions.is_preceded_by(span, ["if"], 5):
        matches.pop(i)
        return

    if postprocessing_functions.is_preceded_by(
        span, ["stay", "staying", "remain", "keep"]
    ):
        matches.pop(i)
        return

    if postprocessing_functions.is_followed_by(span, ["about", "experience"]):
        matches.pop(i)
        return

    mh_terms = [
        "outlet",
        "attitude",
        "encourage",
        "feedback",
        "reinforcement",
        "outlook",
        "mood",
        "mindset",
        "coping",
        "cope",
        "behavior",
        "reinforce",
        "esteem",
    ]

    if postprocessing_functions.sentence_contains(span, mh_terms, regex=False):
        matches.pop(i)
        return


def disambiguate_contact(matcher, doc, i, matches):
    exclude_terms = ["droplet", "precaution", "isolat"]
    (_, start, end) = matches[i]
    span = doc[start:end]

    rslt = postprocessing_functions.sentence_contains(span, exclude_terms, regex=True)
    if rslt is True:
        # print("Removing", span)
        matches.pop(i)
        return


def not_sent_start(matcher, doc, i, matches):
    (_, start, end) = matches[i]
    span = doc[start:end]
    if span.start == span.sent.start:
        matches.pop(i)


def disambiguate_exposure(matcher, doc, i, matches):
    (_, start, end) = matches[i]
    span = doc[start:end]
    if postprocessing_functions.sentence_contains(span, ["tracing", "trace"]):
        matches.pop(i)
        return
    # for text in ["tracing", "trace"]:
    #     if text in span.sent.lower_:
    #         matches.pop(i)
    #         return


def check_no_x_detected(matcher, doc, i, matches):
    """If the modifier 'detected' is preceded by 'no' within a certain window,
    remove it to avoid a false positive.
    Example: 'No flu, pneumonia, or covid-19 detected.'
    """
    (_, start, end) = matches[i]
    span = doc[start:end]
    # Get the entire sentence before the span
    left_start = start
    while True:
        left_start -= 1
        if left_start < 0:
            break
        if doc[left_start].sent != span.sent:
            break
    left_span = doc[left_start:start]
    if "no" in left_span.lower_:
        matches.pop(i)


def check_telephone_notification(matcher, doc, i, matches):
    """If the phrase 'telephone' or 'telehealth' is in the same sentence as 'notified'
        don't consider it a modifier.
        Example to keep: 'Checkup done via telephone because of COVID-19.'
        Example to discard: 'Pt notified via telephone of his positive COVID-19 result.'
    """
    (_, start, end) = matches[i]
    span = doc[start:end]
    if postprocessing_functions.sentence_contains(
        span, ["notify", "notified", "resch"]
    ):
        matches.pop(i)


def disambiguate_active(matcher, doc, i, matches):
    (_, start, end) = matches[i]
    span = doc[start:end]
    if in_parens(span):
        matches.pop(i)
        return

    if start > 0:
        for text in ["stay", "physical"]:
            if text in doc[start - 1].lower_:
                matches.pop(i)
                return


def in_parens(span):
    doc = span.doc
    start, end = span.start, span.end
    if doc[start - 1].text == "(" and doc[end].text == ")":
        return True
    return False


def family_speaker(matcher, doc, i, matches):
    (_, start, end) = matches[i]
    span = doc[start:end]

    # Look following the span
    phrases = ["explained", "told", "informed", "reports", "reported"]
    if span.end != span.sent.end:
        following_end = max(span.end + 2, span.sent.end)
        following_span = doc[span.end : following_end]

        if postprocessing_functions.span_contains(following_span, phrases):
            matches.pop(i)

            return

    communication_phrases = [
        "speak with",
        "spoke ",
        "explain",
        "brought in",
        "discussed with",
        "per\b",
        "decision",
        "contact",
        "contacted",
        "report",
        "\bcall\b",
        "telephone",
        "inform",
    ]

    # Check if this is the main subject of the sentence, in which case they probably tested positive
    # print(span, span.root, span.root.dep_)
    if "nsubj" in span.root.dep_:
        return
    # Otherwise, see if they are preceded by a communication verb
    # Look in the preceding window up to the beginning of the sentence
    if span.sent.start != span.start:
        precede_start = max(span.sent.start, span.start - 6)
        precede_span = doc[precede_start : span.start]

        if postprocessing_functions.span_contains(precede_span, communication_phrases):
            matches.pop(i)
            return
