import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="astir-marker-generator",
    version="0.0.1",
    author="Jinyu Hou",
    author_email="jhou@lunenfeld.ca",
    description=" ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camlab-bioml/astir-marker-generator",
    packages=["astir-marker-generator"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="GPLv3",
    install_requires=[
        "pandas",
        "pyyaml",
        "argparse",
        "os"
    ],
    include_package_data=True,
    scripts=["bin/astir-marker"],
)
