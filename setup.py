from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cm',
    version='0.9.0',
    description='Modern CMake project generator',
    long_description=readme,
    author='Stefan Buschmann',
    author_email='sbusch@sbusch.net',
    url='https://github.com/sbusch42/cm',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    scripts=['cm']
)
