from setuptools import setup, find_packages
from algofresco.version import version
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='algofresco',
    version=version,
    description="A library to visulize algorithms and data structures",
    author="Ahmed Rakan",
    author_email="ar.aldhafeeri11@gmail.com",
    packages=[
        'algofresco', 
        ],
    install_requires=[
        'networkx==3.4.2',
        'matplotlib==3.10.1'
    ],
    test_suite='tests',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
)
