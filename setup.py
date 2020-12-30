from setuptools import setup, find_namespace_packages

# read the contents of the README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cov_bsv",
    version="0.0.1.4",
    description="An NLP pipeline for COVID-19 surveillance used in the Department of Veterans Affairs Biosurveillance.",
    author="alec.chapman",
    author_email="alec.chapman@hsc.utah.edu",
    # packages=["cov_bsv",],
    packages=find_namespace_packages(include=["cov_bsv", "cov_bsv.knowledge_base"]),
    install_requires=[
        "spacy<3.0.0",
        "medspacy==0.1.0.0",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
