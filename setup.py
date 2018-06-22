from setuptools import setup, find_packages


install_requires = []

dev_requires = [
    'pytest==3.5.0',
    'flake8>=3.3.0',
    'pytest-cov>=2.5.1',
    'pip-tools==1.10.1',
]

setup(
    name='pycfmodel',
    version='0.2.0',
    description='A python model for CloudFormation scripts',
    author='Skyscanner Product Security',
    author_email='security@skyscanner.net',
    url='',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={
        'dev': dev_requires,
    }
)
