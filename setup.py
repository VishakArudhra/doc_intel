import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="doc_intel",
    version="0.0.6",
    description="Your solution to cleansing PDF documents for preprocessing for NLP",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/VishakArudhra/detext",
    author="Vishak Arudhra",
    author_email="vishakarudhra@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["doc_intel"],
    include_package_data=True,
    install_requires=["pandas", "Unidecode", "unicodedata2", "clean-text", "Levenshtein", "PyMuPDF", "regex"],
    entry_points={
        "console_scripts": [
            "text_obj=doc_intel.text_laundry:main",
        ]
    },
)