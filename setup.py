from pathlib import Path

from setuptools import setup, find_packages

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "LICENSE") as file:
    _license = file.read()

with open(BASE_DIR / "README.md") as file:
    description = file.read()

setup(
    name="bf-mobilemoney",
    version="0.0.1",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/parice02/bf-mobilemoney",
    description="Library for mobile money payment in Burkina Faso",
    packages=find_packages(include=["mobilemoney"]),
    author="Mohamed ZEBA, Abdoul Kader KABORÉ",
    author_email="<parice02@hotmail.com>, <derokabore@gmail.com>",
    license=_license,
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    requires=["request"],
)
