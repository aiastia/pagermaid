""" Packaging of PagerMaid. """

from setuptools import setup, find_packages
from pip._internal.req import parse_requirements
with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fp:
    install_requires = fp.read()

setup(
    name="pagermaid",
    version="2020.1.post5",
    author="Stykers",
    author_email="stykers@stykers.moe",
    description="A telegram utility daemon.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://katonkeyboard.moe/pagermaid.html",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix"
    ],
    python_requires=">=3.6",
    install_requires=install_requires
)
