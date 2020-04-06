from pathlib import Path

from setuptools import setup, find_namespace_packages


readme = Path(__file__).parent / "README.md"
long_description = readme.read_text()

install_requires = ["pydantic~=1.0"]

dev_requires = ["black==19.3b0", "pytest==3.6.0", "flake8>=3.3.0", "pytest-cov>=2.5.1", "pip-tools==2.0.2"]

docs_requires = ["AutoMacDoc==0.3", "mkdocs-material==4.6.3", "mkdocs==1.1", "mkdocstrings==0.10.0"]

setup(
    name="pycfmodel",
    version="0.7.1",
    description="A python model for CloudFormation scripts",
    author="Skyscanner Product Security",
    author_email="security@skyscanner.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Skyscanner/pycfmodel",
    packages=find_namespace_packages(exclude=("tests", "docs")),
    python_requires=">=3.7",
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={"dev": dev_requires, "docs": docs_requires},
)
