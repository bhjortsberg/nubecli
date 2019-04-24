from setuptools import setup, find_packages

setup(
    name="nubecli",
    version="0.3.0",
    description="Cloud (VPS) command line tool",
    author="Bjorn Hjortsberg",
    author_email="bjorn.hjorgsberg@gmail.com",
    url="https://github.com/bhjortsberg/nubecli",
    packages=find_packages(exclude=["env"]),
    entry_points={
        'console_scripts': [
            'nubecli=nubecli.nubecli:main',
        ]
    }
)

