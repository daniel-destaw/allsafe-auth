import os
from setuptools import setup, find_packages

setup(
    name="allsafe-auth",
    version="1.1.2",
    packages=find_packages(),
    install_requires=[
        "python-ldap>=3.4.0",
        "ldap3>=2.9",
        "qrcode>=8.2",
        "Pillow>=11.2.1",
        "cryptography>=39.0",
        "bcrypt>=4.0.1",
    ],
    author="Daniel Destaw",
    author_email="daniel@allsafe.com",
    description="A complete authentication library including TOTP, HOTP, Active Directory, and more.",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
