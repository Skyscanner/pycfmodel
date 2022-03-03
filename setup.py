from pathlib import Path

from setuptools import find_namespace_packages, setup

readme = Path(__file__).parent / "README.md"
long_description = readme.read_text()

install_requires = ["pydantic~=1.0"]

dev_requires = [
    "black>=22.1.0",
    "flake8>=3.8.3",
    "httpx>=0.14.2",
    "isort>=5.4.2",
    "pip-tools>=2.0.2",
    "pytest>=6.0.1",
    "pytest-cov>=2.10.1",
]

docs_requires = ["AutoMacDoc==0.3", "mkdocs-material==4.6.3", "mkdocs==1.1", "mkdocstrings==0.10.0"]

setup(
    name="pycfmodel",
    version="0.17.1",
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
