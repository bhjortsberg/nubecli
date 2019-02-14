from setuptools import setup

setup(
    name="Cloud tool",
    version="0.2.0",
    description="Cloud command line tool",
    author="Bjorn Hjortsberg",
    packages=["."],
    entry_points={
        'console_scripts': [
            'ccli=ccli:main',
        ],
    }
)

