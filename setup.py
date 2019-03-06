from setuptools import setup, find_packages

setup(
    name="Cloud tool",
    version="0.2.0",
    description="Cloud command line tool",
    author="Bjorn Hjortsberg",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ccli=ccli:main',
        ],
    }
)

