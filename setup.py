from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='dedact_metadata',
    version='0.1.0',
    description='A package that analyses input for different types of meta-data',
    long_description=readme,
    author='Silvia van Wingerden',
    author_email='silvia@dedact.nl',
    url='https://github.com/Silviavw/dedact_metadata',
    packages=find_packages(exclude=('tests', 'docs'))
)
