import re

from setuptools import find_packages, setup


def get_required():

    with open("requirements/main.txt", "r") as f:
        reqs = f.readlines()

    clean_reqs = [x for x in reqs if re.search(r"^\w", x)]
    return [x.split('==')[0] for x in clean_reqs]


setup(
    name="entitychooser",
    version="0.1",
    packages=find_packages(),
    install_requires=get_required(),
    author="ann-cooper",
    author_email="owlshead@gmail.com",
    description="A tool to prepare pdfs for redaction and choose entities to redact.",
)
