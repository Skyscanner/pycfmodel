from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = []

dev_requires = [
    'pytest==3.6.0',
    'flake8>=3.3.0',
    'pytest-cov>=2.5.1',
    'pip-tools==2.0.2',
]

setup(
    name='pycfmodel',
    version='0.2.11',
    description='A python model for CloudFormation scripts',
    author='Skyscanner Product Security',
    author_email='security@skyscanner.net',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Skyscanner/pycfmodel',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={
        'dev': dev_requires,
    }
)
