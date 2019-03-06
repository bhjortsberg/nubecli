from setuptools import setup

setup(
    name="nubecli",
    version="0.3.0",
    description="Cloud (VPS) command line tool",
    author="Bjorn Hjortsberg",
    packages=[".", "config"],
    entry_points={
        'console_scripts': [
            'nubecli=nubecli:main',
        ],
    }
)

