from distutils.core import setup

from setuptools import find_packages
import os 

folder = os.path.dirname(os.path.realpath(__file__))
requirementPath = os.path.join(folder,'/requirements.txt')

install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()


setup(
    name="Package Name",
    version="1.0",
    packages=find_packages(),
    package_data={p: ["*"] for p in find_packages()},
    url="",
    license="",
    install_requires=install_requires,
    python_requires=">=3.7.1",
    author="nprime496",
    description="This is a ligthweight two-player game",
)