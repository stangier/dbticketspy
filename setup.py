from setuptools import find_packages, setup

setup(
    name="dbticketspy",
    packages=find_packages(include=["dbticketspy"]),
    version="0.2.0",
    description="A Python library to query the DB website for ticket information.",
    author="Lorenz Stangier",
    license="MIT",
    install_requires=["requests"],
)