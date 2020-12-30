import spacy
import medspacy

from spacy.tokens import Span, Token

from .document_classifier import DocumentClassifier

from .knowledge_base import preprocess_rules
from .knowledge_base import concept_tag_rules
from .knowledge_base import target_rules
from .knowledge_base import section_rules
from .knowledge_base import context_rules
from .knowledge_base import postprocess_rules
# from .knowledge_base import *

DEFAULT_PIPENAMES = [
    "preprocessor",
    "tagger",
    "parser",
    "concept_tagger",
    "target_matcher",
    "sectionizer",
    "context",
    "postprocessor",
    "document_classifier"
]

CONTEXT_MAPPING = {
    "NEGATED_EXISTENCE": {"is_negated": True},
    "FUTURE/HYPOTHETICAL": {"is_future": True},
    "HISTORICAL": {"is_historical": True},
    "DEFINITE_POSITIVE_EXISTENCE": {"is_positive": True},
    "ADMISSION": {"is_positive": True},
    "NOT_RELEVANT": {"is_not_relevant": True},
    "UNCERTAIN": {"is_uncertain": True},
    "UNLIKELY": {"is_uncertain": True},
    "SCREENING": {"is_screening": True},
    "OTHER_EXPERIENCER": {"is_other_experiencer": True},
    "CONTACT": {"is_other_experiencer": True},
    "PATIENT_EXPERIENCER": {"is_other_experiencer": False, "is_positive": True},
}

SECTION_ATTRS = {
    "diagnoses": {"is_positive": True},
    "observation_and_plan": {"is_positive": True},
    "past_medical_history": {"is_positive": True},
    "problem_list": {"is_positive": True},
}


def _set_attributes():
    Span.set_extension("is_future", default=False, force=True)
    Span.set_extension("is_historical", default=False, force=True)
    Span.set_extension(
        "is_positive", default=False, force=True
    )  # Explicitly has a positive indicator
    Span.set_extension(
        "is_not_relevant", default=False, force=True
    )  # News reports, etc..
    Span.set_extension("is_negated", default=False, force=True)
    Span.set_extension("is_uncertain", default=False, force=True)
    Span.set_extension("is_screening", default=False, force=True)
    Span.set_extension("is_other_experiencer", default=False, force=True)
    Span.set_extension("concept_tag", default="", force=True)

def load(model="default", enable=None, disable=None, load_rules=True, set_attributes=True):
    """Load a spaCy language object with cov_bsv pipeline components.
    By default, the base model will be 'en_core_web_sm' with the 'tagger'
    and 'parser' pipeline components, supplemented with the following custom
    components:
        - preprocessor (set to be nlp.tokenizer): Modifies the preprocessed text and returns
            a tokenized Doc. Preprocess rules are defined in cov_bsv.knowledge_base.preprocess_rules
        - concept_tagger: Assigns a semantic tag in a custom attribute "token._.concept_tag"
            to each Token in a Doc, which helps with concept extraction and normalization.
            Concept tag rules are defined in cov_bsv.knowledge_base.concept_tag_rules.
        - target_matcher: Extracts spans to doc.ents using extended rule-based matching.
            Target rules are defined in cov_bsv.knowledge_base.target_rules.
        - sectionizer: Identifies note section headers in the text and assigns section titles to
            entities and tokens contained in that section. Section patterns are defined in
            cov_bsv.knowledge_base.section_patterns.
        - context: Identifies semantic modifiers of entities and asserts attributes such as
            positive status, negation, and other experiencier. Context rules are defined in
            cov_bsv.knowledge_base.context_rules.
        - postprocessor: Modifies or removes the entity based on business logic. This handles
            special cases or complex logic using the results of earlier entities. Postprocess rules
            are defined in cov_bsv.knowledge_base.postprocess_rules.
        - document_classifier: Assigns a label of "POS", "UNK", or "NEG" to the doc._.cov_classification.
            A document will be classified as positive if it has at least one positive, non-excluded entity.

    Args:
        model: The name of the base spaCy model to load. If "default" will load the tagger and parser
            from "en_core_web_sm".
        enable (iterable or None): A list of component names to include in the pipeline.
        If None, will include all pipeline components listed above.
        disable (iterable or None): A list of component names to exclude.
            Cannot be set if `enable` is not None.
        load_rules (bool): Whether or not to include default rules for custom components. Default True.
        set_attributes (bool): Whether or not to register custom attributes to spaCy classes. If load_rules is True,
            this will automatically be set to True because the rules in the knowledge base rely on these custom attributes.
            The following extensions are registered (all defaults are False unless specified):
                Span._.is_future
                Span._.is_historical
                Span._.is_positive
                Span._.is_not_relevant
                Span._.is_negated
                Span._.is_uncertain
                Span._.is_screening
                Span._.is_other_experiencer
                Span._.concept_tag (default "")

    Returns:
        nlp: a spaCy Language object
    """
    if enable is not None and disable is not None:
        raise ValueError("Either `enable` or `disable` must be None.")
    if disable is not None:
        # If there's a single pipe name, nest it in a set
        if isinstance(disable, str):
            disable = {disable}
        else:
            disable = set(disable)
        enable = set(DEFAULT_PIPENAMES).difference(set(disable))
    elif enable is not None:
        if isinstance(enable, str):
            enable = {enable}
        else:
            enable = set(enable)
        disable = set(DEFAULT_PIPENAMES).difference(enable)
    else:
        enable = DEFAULT_PIPENAMES
        disable = set()

    if model == "default":
        model = "en_core_web_sm"
        disable.add("ner")


    if set_attributes:
        _set_attributes()

    import spacy
    nlp = spacy.load(model, disable=disable)

    if "preprocessor" in enable:
        from medspacy.preprocess import Preprocessor

        preprocessor = Preprocessor(nlp.tokenizer)
        if load_rules:
            preprocessor.add(preprocess_rules)
        nlp.tokenizer = preprocessor

    if "concept_tagger" in enable:
        from spacy.tokens import Token

        Token.set_extension("concept_tag", default="", force=True)
        from medspacy.ner import ConceptTagger

        concept_tagger = ConceptTagger(nlp)
        if load_rules:
            for (_, rules) in concept_tag_rules.items():
                concept_tagger.add(rules)
        nlp.add_pipe(concept_tagger)

    if "target_matcher" in enable:
        from medspacy.ner import TargetMatcher

        target_matcher = TargetMatcher(nlp)
        if load_rules:
            for (_, rules) in target_rules.items():
                target_matcher.add(rules)
        nlp.add_pipe(target_matcher)

    if "sectionizer" in enable:
        from medspacy.section_detection import Sectionizer
        sectionizer = Sectionizer(nlp, rules=None, add_attrs=SECTION_ATTRS)
        if load_rules:
            sectionizer.add(section_rules)
        nlp.add_pipe(sectionizer)

    if "context" in enable:
        from medspacy.context import ConTextComponent

        context = ConTextComponent(
            nlp,
            add_attrs=CONTEXT_MAPPING,
            rules=None,
            remove_overlapping_modifiers=True,
        )
        if load_rules:
            context.add(context_rules)
        nlp.add_pipe(context)

    if "postprocessor" in enable:
        from medspacy.postprocess import Postprocessor

        postprocessor = Postprocessor(debug=False)
        if load_rules:
            postprocessor.add(postprocess_rules)
        nlp.add_pipe(postprocessor)

    if "document_classifier" in enable:
        document_classifier = DocumentClassifier()
        nlp.add_pipe(document_classifier)

    return nlp


def visualize_doc(doc, document_id=None, jupyter=True, colors=None):
    """Display a processed doc using an NER-style spaCy visualization.
    By default, this will highlight entities, modifiers, and section titles
    and will display the document classification as a header.

    doc: A spaCy Doc which has been processed by the cov_bsv pipeline.
    document_id: An optional document identifier to be displayed as a header.
    jupyter (bool): If True, will display the resulting HTML inline in a notebook.
        If False, will return the HTML as a string.
    """
    from IPython.display import display, HTML
    from medspacy.visualization import visualize_ent

    html = "<h2>Document Classification: {0}</h2>".format(doc._.cov_classification)
    if document_id is not None:
        html += "<h3>Document ID: {0}</h3>".format(document_id)
    html += visualize_ent(doc, colors=colors, jupyter=False)
    if jupyter is True:
        display(HTML(html))
    else:
        return html
