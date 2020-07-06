from medspacy.preprocess import PreprocessingRule
import re

preprocess_rules = [
    PreprocessingRule(
        re.compile("Has the patient been diagnosed with COVID-19\? Y/N"),
        desc="Remove template questionnaire (pseudo example)",
    ),
]
