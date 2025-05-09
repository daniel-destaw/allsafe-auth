import os
from setuptools import setup, find_packages

# Automatically read requirements.txt
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="allsafe-authentication",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requirements,
    author="Daniel Destaw",
    author_email="daniel@allsafe.com",
    description="A complete authentication library including TOTP, HOTP, Active Directory, and more.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
